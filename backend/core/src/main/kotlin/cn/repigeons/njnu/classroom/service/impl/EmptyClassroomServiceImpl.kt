package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.CorrectionRecord
import cn.repigeons.njnu.classroom.mbg.model.FeedbackMetadataRecord
import cn.repigeons.njnu.classroom.model.EmptyClassroom
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.EmptyClassroomService
import cn.repigeons.njnu.classroom.service.SpiderService
import cn.repigeons.njnu.classroom.util.EmailUtil
import cn.repigeons.njnu.classroom.util.GsonUtil
import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.JSONObject
import com.alibaba.fastjson.serializer.SerializerFeature
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.redisson.api.RedissonClient
import org.springframework.beans.factory.annotation.Value
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service
import java.util.*

@Service
open class EmptyClassroomServiceImpl(
    private val redissonClient: RedissonClient,
    private val cacheService: CacheService,
    private val spiderService: SpiderService,
    private val proMapper: ProMapper,
    private val feedbackMetadataMapper: FeedbackMetadataMapper,
    private val correctionMapper: CorrectionMapper,
    @Value("\${spring.mail.receivers}")
    val receivers: Array<String>,
    @Value("\${env}") private val env: String
) : EmptyClassroomService {
    override fun getEmptyClassrooms(jxl: String, day: Weekday?, jc: Short): JsonResponse {
        if (day == null) return JsonResponse(
            status = Status.BAD_REQUEST,
            message = "无效参数: [day]"
        )
        if (jc !in 1..12) return JsonResponse(
            status = Status.BAD_REQUEST,
            message = "无效参数: [jc]"
        )
        val rMap = redissonClient.getMap<String, String>("empty")
        val classrooms = rMap["$jxl:${day.value}"]?.let {
            GsonUtil.fromJson<List<EmptyClassroom>>(it)
        } ?: return JsonResponse(
            status = Status.BAD_REQUEST,
            message = "无效参数: [jxl]"
        )
        val result = classrooms.filter { classroom ->
            jc in classroom.jcKs..classroom.jcJs
        }
        return JsonResponse(data = result)
    }

    @Async
    override fun feedback(
        jxl: String,
        day: Weekday,
        jc: Short,
        results: List<EmptyClassroom>,
        index: Int
    ) {
        if (env != "pro") return
        val item = results[index]

        // 检查缓存一致性
        val count = proMapper.count {
            where(ProDynamicSqlSupport.Pro.day, isEqualTo(day.value))
            and(ProDynamicSqlSupport.Pro.jcKs, isEqualTo(item.jcKs))
            and(ProDynamicSqlSupport.Pro.jcJs, isEqualTo(item.jcJs))
            and(ProDynamicSqlSupport.Pro.jasdm, isEqualTo(item.jasdm))
            and(ProDynamicSqlSupport.Pro.zylxdm, isEqualTo(item.zylxdm))
        }
        if (count == 0L) {
            cacheService.flush()
            return
        }

        val obj = JSONObject().apply {
            set("jc", jc)
            set("item", item)
            set("index", index)
            set("results", results)
        }
        val detail = JSON.toJSONString(
            obj,
            SerializerFeature.PrettyFormat,
            SerializerFeature.WriteMapNullValue
        )
        val subject = "【南师教室】用户反馈：" +
                "$jxl ${item.jsmph}教室 " +
                "${item.jcKs}-${item.jcJs}节有误" +
                "（当前为第${jc}节）"

        // 检查数据库一致性
        if (!spiderService.checkWithEhall(item.jasdm, day, jc, item.zylxdm)) {
            spiderService.run()
            val content = "验证一站式平台：数据不一致\n" +
                    "操作方案：更新数据库\n" +
                    "反馈数据详情：$detail"
            EmailUtil.send(
                nickname = "南师教室",
                subject = subject,
                content = content,
                receivers = receivers
            )
            return
        }

        // 记录反馈内容
        if (item.zylxdm != "00") {
            val content = "验证一站式平台：数据一致（非空教室）\n" +
                    "操作方案：${null}\n" +
                    "反馈数据详情：$detail"
            EmailUtil.send(
                nickname = "南师教室",
                subject = subject,
                content = content,
                receivers = receivers
            )
            return
        } else {
            val map = autoCorrect(
                jxl = jxl,
                jasdm = item.jasdm,
                jsmph = item.jsmph,
                day = day,
                jc = jc
            )
            val weekCount = map["weekCount"]!!
            val totalCount = map["totalCount"]!!
            val content = "验证一站式平台：数据一致\n" +
                    "上报计数：${totalCount}\n" +
                    "本周计数：${weekCount}\n" +
                    "操作方案：${if (weekCount == totalCount) null else "自动纠错"}\n" +
                    "反馈数据详情：$detail"
            EmailUtil.send(
                nickname = "南师教室",
                subject = subject,
                content = content,
                receivers = receivers
            )
            return
        }
    }

    private fun autoCorrect(jxl: String, jasdm: String, jsmph: String, day: Weekday, jc: Short): Map<String, Long> {
        val record = FeedbackMetadataRecord(
            jc = jc,
            jasdm = jasdm,
            time = Date()
        )
        feedbackMetadataMapper.insert(record)
        val statistic = feedbackMetadataMapper.statistic(jasdm, mapDay(day), jc)
        val weekCount = statistic.lastOrNull() ?: 0
        val totalCount = statistic.sumOf { it }
        if (weekCount != totalCount)
            correctionMapper.insertSelective(
                CorrectionRecord(
                    day = day.value,
                    jxlmc = jxl,
                    jsmph = jsmph,
                    jasdm = jasdm,
                    jcKs = jc,
                    jcJs = jc,
                    jyytms = "占用",
                    kcm = "####占用"
                )
            )
        return mapOf(
            Pair("weekCount", weekCount),
            Pair("totalCount", totalCount),
        )
    }

    private fun mapDay(day: Weekday): Int {
        return when (day) {
            Weekday.Sunday -> 1
            Weekday.Monday -> 2
            Weekday.Tuesday -> 3
            Weekday.Wednesday -> 4
            Weekday.Thursday -> 5
            Weekday.Friday -> 6
            Weekday.Saturday -> 7
            else -> throw IllegalArgumentException()
        }
    }
}