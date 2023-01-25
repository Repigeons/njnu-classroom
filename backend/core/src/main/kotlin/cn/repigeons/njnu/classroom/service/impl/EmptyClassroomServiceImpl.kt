package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.commons.redisTemplate.RedisService
import cn.repigeons.commons.utils.GsonUtils
import cn.repigeons.njnu.classroom.enumerate.Weekday
import cn.repigeons.njnu.classroom.mbg.dao.FeedbackDAO
import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.CorrectionRecord
import cn.repigeons.njnu.classroom.mbg.model.FeedbackRecord
import cn.repigeons.njnu.classroom.model.EmptyClassroom
import cn.repigeons.njnu.classroom.service.EmptyClassroomService
import cn.repigeons.njnu.classroom.service.SpiderService
import cn.repigeons.njnu.classroom.util.EmailUtil
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import java.util.*
import java.util.concurrent.CompletableFuture

@Service
class EmptyClassroomServiceImpl(
    private val redisService: RedisService,
    private val spiderService: SpiderService,
    private val timetableMapper: TimetableMapper,
    private val feedbackMapper: FeedbackMapper,
    private val feedbackDAO: FeedbackDAO,
    private val correctionMapper: CorrectionMapper,
    @Value("\${spring.mail.receivers}")
    val receivers: Array<String>
) : EmptyClassroomService {
    override fun getEmptyClassrooms(jxl: String, weekday: Weekday?, jc: Short): List<EmptyClassroom> {
        requireNotNull(weekday) { "无效参数: [weekday]" }
        require(jc in 1..12) { "无效参数: [jc]" }
        val classrooms = requireNotNull(redisService.hGet("empty", "$jxl:${weekday.name}") as List<*>?) {
            "无效参数: [jxl]"
        }
        return classrooms.mapNotNull { classroom ->
            classroom as EmptyClassroom
            if (jc in classroom.jcKs..classroom.jcJs)
                classroom
            else
                null
        }
    }

    override fun feedback(
        jxlmc: String,
        weekday: Weekday,
        jc: Short,
        results: List<EmptyClassroom>,
        index: Int
    ): CompletableFuture<*> = CompletableFuture.supplyAsync {
        val item = results[index]

        // 检查缓存一致性
        val count = timetableMapper.count {
            where(TimetableDynamicSqlSupport.Timetable.weekday, isEqualTo(weekday.name))
            and(TimetableDynamicSqlSupport.Timetable.jcKs, isEqualTo(item.jcKs))
            and(TimetableDynamicSqlSupport.Timetable.jcJs, isEqualTo(item.jcJs))
            and(TimetableDynamicSqlSupport.Timetable.jasdm, isEqualTo(item.jasdm))
            and(TimetableDynamicSqlSupport.Timetable.zylxdm, isEqualTo(item.zylxdm))
        }
        if (count == 0L) {
            spiderService.flushCache()
            return@supplyAsync
        }

        val obj = mapOf(
            Pair("jc", jc),
            Pair("item", item),
            Pair("index", index),
            Pair("results", results)
        )
        val detail = GsonUtils.toJson(obj)
        val subject = "【南师教室】用户反馈：" +
                "$jxlmc ${item.jsmph}教室 " +
                "${item.jcKs}-${item.jcJs}节有误" +
                "（当前为第${jc}节）"

        // 检查数据库一致性
        if (!spiderService.checkWithEhall(item.jasdm, weekday, jc, item.zylxdm)) {
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
            return@supplyAsync
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
            return@supplyAsync
        } else {
            val map = autoCorrect(
                jxl = jxlmc,
                jasdm = item.jasdm,
                jsmph = item.jsmph,
                weekday = weekday,
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
            return@supplyAsync
        }
    }

    private fun autoCorrect(jxl: String, jasdm: String, jsmph: String, weekday: Weekday, jc: Short): Map<String, Long> {
        val record = FeedbackRecord(
            jc = jc,
            jasdm = jasdm,
            time = Date()
        )
        feedbackMapper.insert(record)
        val statistic = feedbackDAO.statistic(jasdm, mapDay(weekday), jc)
        val weekCount = statistic.lastOrNull() ?: 0
        val totalCount = statistic.sumOf { it }
        if (weekCount != totalCount)
            correctionMapper.insertSelective(
                CorrectionRecord(
                    weekday = weekday.name,
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

    private fun mapDay(weekday: Weekday) = when (weekday) {
        Weekday.Sun -> 1
        Weekday.Mon -> 2
        Weekday.Tue -> 3
        Weekday.Wed -> 4
        Weekday.Thu -> 5
        Weekday.Fri -> 6
        Weekday.Sat -> 7
    }
}