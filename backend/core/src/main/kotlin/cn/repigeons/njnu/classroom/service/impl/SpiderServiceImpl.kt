package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.CorrectionRecord
import cn.repigeons.njnu.classroom.mbg.model.DevRecord
import cn.repigeons.njnu.classroom.mbg.model.JasRecord
import cn.repigeons.njnu.classroom.mbg.model.KcbRecord
import cn.repigeons.njnu.classroom.model.TimeInfo
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.CookieService
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.service.SpiderService
import cn.repigeons.njnu.classroom.util.GsonUtil
import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.JSONArray
import com.alibaba.fastjson.JSONObject
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.redisson.api.RedissonClient
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit
import kotlin.concurrent.thread

@Service
open class SpiderServiceImpl(
    private val redissonClient: RedissonClient,
    private val redisService: RedisService,
    private val cacheService: CacheService,
    private val cookieService: CookieService,
    private val correctionMapper: CorrectionMapper,
    private val jasMapper: JasMapper,
    private val kcbMapper: KcbMapper,
    private val devMapper: DevMapper,
    private val proMapper: ProMapper,
    @Value("\${spring.profiles.active}")
    private val env: String
) : SpiderService {
    private val logger = LoggerFactory.getLogger(javaClass)
    private val rqDateFormat = SimpleDateFormat("yyyy-MM-dd")
    private lateinit var httpClient: OkHttpClient

    @Async
    override fun run() {
        val rLock = redissonClient.getLock("lock:spider")
        try {
            if (rLock.tryLock(1, 60 * 60, TimeUnit.SECONDS)) {
                logger.info("开始课程信息收集工作...")
                this.actRun()
            } else {
                logger.info("课程信息收集工作已处于运行中...")
            }
        } finally {
            rLock?.unlock()
        }
        cacheService.flush()
    }

    private fun actRun() {
        val startTime = Date()

        val cookies = cookieService.getCookies()
        logger.info("开始采集基础信息...")
        httpClient = cookieService.getHttpClient(cookies)
        val timeInfo = getTimeInfo()
        val buildingInfo = getAcademicBuildingInfo()
        logger.info("基础信息采集完成.")

        logger.info("开始采集课程信息...")
        kcbMapper.truncate()
        buildingInfo.forEach { (buildingName, classroomList) ->
            logger.info("开始查询教学楼[{}]...", buildingName)
            classroomList.map { classroom ->
                thread {
                    logger.debug("正在查询教室[{}]...", classroom.jasmc)
                    getClassInfo(classroom, timeInfo)
                }
            }.forEach { thread ->
                thread.join()
            }
        }
        logger.info("课程信息采集完成.")
        devMapper.truncate()
        devMapper.cloneFromKcb()
        logger.info("开始校正数据...")
        correctData()
        logger.info("数据校正完成...")
        logger.info("开始归并数据...")
        mergeData()
        logger.info("数据归并完成...")

        if (env == "pro") {
            logger.info("Copy to `pro` from `dev`.")
            proMapper.truncate()
            proMapper.cloneFromDev()
        }

        val endTime = Date()
        logger.info("本轮课程信息收集工作成功完成. 共计耗时 {} 秒", (endTime.time - startTime.time) / 1000)
    }

    private fun getTimeInfo(): TimeInfo {
        val result = redisService["spider:time"]?.let {
            GsonUtil.fromJson<TimeInfo>(it)
        } ?: let {
            val timeInfo = TimeInfo()
            val request1 = Request.Builder()
                .url("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxdqxnxq.do")
                .build()
            val response1 = httpClient.newCall(request1).execute()
            val result1 = response1.body()?.string()
            val data1 = JSON.parseObject(result1)
                .getJSONObject("datas")
                .getJSONObject("cxdqxnxq")
                .getJSONArray("rows")
                .getJSONObject(0)
            timeInfo.XNXQDM = data1.getString("DM")
            timeInfo.XNDM = data1.getString("XNDM")
            timeInfo.XQDM = data1.getString("XQDM")

            val requestBody2 = FormBody.Builder()
                .add("XN", data1.getString("XNDM"))
                .add("XQ", data1.getString("XQDM"))
                .add("RQ", rqDateFormat.format(Date()))
                .build()
            val request2 = Request.Builder()
                .url("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do")
                .post(requestBody2)
                .build()
            val response2 = httpClient.newCall(request2).execute()
            val result2 = response2.body()?.string()
            val data2 = JSON.parseObject(result2)
                .getJSONObject("datas")
                .getJSONObject("cxrqdydzcxq")
                .getJSONArray("rows")
                .getJSONObject(0)
            timeInfo.ZC = data2.getString("ZC").toInt()
            timeInfo.ZZC = data2.getString("ZZC").toInt()

            val requestBody3 = FormBody.Builder()
                .add("XN", data1.getString("XNDM"))
                .add("XQ", data1.getString("XQDM"))
                .add("RQ", rqDateFormat.format(Date()))
                .build()
            val request3 = Request.Builder()
                .url("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do")
                .post(requestBody3)
                .build()
            val response3 = httpClient.newCall(request3).execute()
            val result3 = response3.body()?.string()
            val data3 = JSON.parseObject(result3)
                .getJSONObject("datas")
                .getJSONObject("cxxljc")
                .getJSONArray("rows")
                .getJSONObject(0)
            timeInfo.ZJXZC = data3.getString("ZJXZC").toInt()

            redisService.set(
                "spider:time",
                GsonUtil.toJson(timeInfo),
                3 * 24 * 3600
            )
            timeInfo
        }
        logger.debug("Time info = {}", result)
        return result
    }

    private fun getAcademicBuildingInfo(): Map<String, List<JasRecord>> {
        val result = redisService["spider:building"]?.let {
            GsonUtil.fromJson<Map<String, List<JasRecord>>>(it)
        } ?: let {
            val building = jasMapper.select {}
                .groupBy { it.jxldmDisplay!! }
            building.values.forEach {
                it.sortedBy { record ->
                    record.jasmc
                }
            }

            redisService.set(
                "spider:building",
                GsonUtil.toJson(building),
                3 * 24 * 3600
            )
            building
        }
        logger.debug("Building info = {}", result)
        return result
    }

    private fun getClassInfo(classroom: JasRecord, timeInfo: TimeInfo) {
        val thisWeek = timeInfo.ZC
        val nextWeek = if (timeInfo.ZC < timeInfo.ZJXZC) timeInfo.ZC + 1 else timeInfo.ZJXZC
        val kcb = getKcb(timeInfo.XNXQDM, thisWeek.toString(), classroom.jasdm!!)
        if (nextWeek != thisWeek) {
            val kcb2 = getKcb(timeInfo.XNXQDM, nextWeek.toString(), classroom.jasdm!!)
            val weekday = (Calendar.getInstance().get(Calendar.DAY_OF_WEEK) + 4) % 7
            for (day in 0..weekday) {
                kcb[day] = kcb2[day]
            }
        }
        for (day in 0..6) {
            kcb.getJSONArray(day).forEach { row ->
                row as JSONObject
                val jc = row.getString("JC").split(',')
                val kcbRecord = KcbRecord(
                    jxlmc = classroom.jxldmDisplay,
                    jsmph = classroom.jasmc?.replace(Regex("^${classroom.jxldmDisplay}"), "")?.trim(),
                    jasdm = classroom.jasdm,
                    skzws = classroom.skzws,
                    zylxdm = if (row.getString("ZYLXDM").isNullOrBlank()) "00" else row.getString("ZYLXDM"),
                    jcKs = jc.firstOrNull()?.toShort(),
                    jcJs = jc.lastOrNull()?.toShort(),
                    day = mapDay(day).value,
                    sfyxzx = classroom.sfyxzx,
                    jyytms = if (row.getString("JYYTMS").isNullOrBlank()) "" else row.getString("JYYTMS"),
                    kcm = if (row.getString("KCM").isNullOrBlank()) "" else row.getString("KCM"),
                )
                kcbMapper.insert(kcbRecord)
            }
        }
    }

    private fun getKcb(xnxqdm: String, week: String, jasdm: String): JSONArray {
        val requestBody = FormBody.Builder()
            .add("XNXQDM", xnxqdm)
            .add("ZC", week)
            .add("JASDM", jasdm)
            .build()
        val request = Request.Builder()
            .url("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do")
            .post(requestBody)
            .build()
        val response = httpClient.newCall(request).execute()
        val result = response.body()?.string()
        val data = JSON.parseObject(result)
            .getJSONObject("datas")
            .getJSONObject("cxyzjskjyqk")
            .getJSONArray("rows")
            .getJSONObject(0)
        return data.getJSONArray("BY1")
    }

    private fun correctData() {
        val corrections = redisService["spider:corrections"]?.let {
            GsonUtil.fromJson<List<CorrectionRecord>>(it)
        } ?: let {
            val corrections = correctionMapper.select {}
            redisService.set(
                "spider:corrections",
                GsonUtil.toJson(corrections),
                3 * 24 * 3600
            )
            corrections
        }
        logger.debug("Corrections = {}", corrections)

        corrections.forEach { record ->
            if (record.jcKs!! < record.jcJs!!) {
                for (jc in record.jcKs!! until record.jcJs!!)
                    devMapper.delete {
                        where(DevDynamicSqlSupport.Dev.day, isEqualTo(record.day))
                        and(DevDynamicSqlSupport.Dev.jasdm, isEqualTo(record.jasdm))
                        and(DevDynamicSqlSupport.Dev.jcKs, isEqualTo(jc.toShort()))
                        and(DevDynamicSqlSupport.Dev.jcJs, isEqualTo(jc.toShort()))
                    }
            }
            devMapper.update {
                set(DevDynamicSqlSupport.Dev.skzws).equalTo(record.skzws)
                set(DevDynamicSqlSupport.Dev.zylxdm).equalTo(record.zylxdm)
                set(DevDynamicSqlSupport.Dev.jyytms).equalTo(record.jyytms)
                set(DevDynamicSqlSupport.Dev.kcm).equalTo(record.kcm)
                set(DevDynamicSqlSupport.Dev.jcKs).equalTo(record.jcKs)
                where(DevDynamicSqlSupport.Dev.day, isEqualTo(record.day))
                and(DevDynamicSqlSupport.Dev.jasdm, isEqualTo(record.jasdm))
                and(DevDynamicSqlSupport.Dev.jcKs, isEqualTo(record.jcJs))
                and(DevDynamicSqlSupport.Dev.jcJs, isEqualTo(record.jcJs))
            }
        }
    }

    private fun mergeData() {
        val data = devMapper.select {
            orderBy(
                DevDynamicSqlSupport.Dev.day,
                DevDynamicSqlSupport.Dev.jxlmc,
                DevDynamicSqlSupport.Dev.jsmph,
                DevDynamicSqlSupport.Dev.jcJs,
            )
        }.groupBy {
            it.jxlmc!!
        }
        val result = mutableMapOf<String, MutableList<DevRecord>>()
        data.map { (jxlmc, records) ->
            thread {
                logger.info("[{}] 开始归并...", jxlmc)
                val classrooms = mutableListOf<DevRecord>()
                result[jxlmc] = classrooms
                records.forEach { record ->
                    if (classrooms.isNotEmpty()
                        && record.jasdm == classrooms.last().jasdm
                        && record.zylxdm == "00"
                        && classrooms.last().zylxdm == "00"
                    )
                        classrooms.last().jcJs = record.jcJs
                    else
                        classrooms.add(record)
                }
            }
        }.forEach { thread ->
            thread.join()
        }
        // 清空数据库
        devMapper.truncate()
        // 重新插入数据库
        result.forEach { (jxlmc, records) ->
            records.forEach { record ->
                devMapper.insert(record)
            }
            logger.info("[{}] 归并完成.", jxlmc)
        }
    }

    override fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String): Boolean {
        val cookies = cookieService.getCookies()
        httpClient = cookieService.getHttpClient(cookies)
        val timeInfo = getTimeInfo()
        val kcb = getKcb(timeInfo.XNXQDM, timeInfo.ZC.toString(), jasdm)
        kcb.getJSONArray(mapDay(day)).forEach { row ->
            row as JSONObject
            val bool1 = jc.toString() in row.getString("JC").split(',')
            val bool2 = row.getString("ZYLXDM") == zylxdm || row.getString("ZYLXDM").isBlank()
            if (bool1 && bool2)
                return true
        }
        return false
    }

    private fun mapDay(day: Int): Weekday {
        return when (day) {
            0 -> Weekday.Monday
            1 -> Weekday.Tuesday
            2 -> Weekday.Wednesday
            3 -> Weekday.Thursday
            4 -> Weekday.Friday
            5 -> Weekday.Saturday
            6 -> Weekday.Sunday
            else -> throw IllegalArgumentException()
        }
    }

    private fun mapDay(day: Weekday): Int {
        return when (day) {
            Weekday.Monday -> 0
            Weekday.Tuesday -> 1
            Weekday.Wednesday -> 2
            Weekday.Thursday -> 3
            Weekday.Friday -> 4
            Weekday.Saturday -> 5
            Weekday.Sunday -> 6
            else -> throw IllegalArgumentException()
        }
    }
}