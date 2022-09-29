package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.CorrectionRecord
import cn.repigeons.njnu.classroom.mbg.model.JasRecord
import cn.repigeons.njnu.classroom.mbg.model.KcbRecord
import cn.repigeons.njnu.classroom.mbg.model.TimetableRecord
import cn.repigeons.njnu.classroom.model.KcbItem
import cn.repigeons.njnu.classroom.model.TimeInfo
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.CookieService
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.service.SpiderService
import cn.repigeons.njnu.classroom.util.GsonUtil
import com.google.gson.JsonParser
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import org.apache.ibatis.session.ExecutorType
import org.apache.ibatis.session.SqlSessionFactory
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.redisson.api.RedissonClient
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.CompletableFuture

@Service
open class SpiderServiceImpl(
    private val redissonClient: RedissonClient,
    private val redisService: RedisService,
    private val cacheService: CacheService,
    private val cookieService: CookieService,
    private val correctionMapper: CorrectionMapper,
    private val jasMapper: JasMapper,
    private val kcbMapper: KcbMapper,
    private val timetableMapper: TimetableMapper,
    private val sqlSessionFactory: SqlSessionFactory
) : SpiderService {
    private val logger = LoggerFactory.getLogger(javaClass)
    private val rqDateFormat = SimpleDateFormat("yyyy-MM-dd")
    private lateinit var httpClient: OkHttpClient

    @Async
    override fun run() {
        val lock = redissonClient.getLock("lock:spider")
        if (!lock.tryLock()) {
            logger.info("课程信息收集工作已处于运行中...")
            return
        }
        try {
            logger.info("开始课程信息收集工作...")
            this.actRun()
            cacheService.flush()
        } finally {
            lock.unlock()
        }
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
                logger.debug("正在查询教室[{}]...", classroom.jasmc)
                getClassInfo(classroom, timeInfo)
            }.forEach { future -> future.join() }
        }
        logger.info("课程信息采集完成.")
        timetableMapper.truncate()
        timetableMapper.cloneFromKcb()
        logger.info("开始校正数据...")
        correctData()
        logger.info("数据校正完成...")
        logger.info("开始归并数据...")
        mergeData()
        logger.info("数据归并完成...")
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
            val data1 = JsonParser.parseString(result1)
                .asJsonObject
                .getAsJsonObject("datas")
                .getAsJsonObject("cxdqxnxq")
                .getAsJsonArray("rows")
                .get(0)
                .asJsonObject
            timeInfo.XNXQDM = data1.get("DM").asString
            timeInfo.XNDM = data1.get("XNDM").asString
            timeInfo.XQDM = data1.get("XQDM").asString

            val requestBody2 = FormBody.Builder()
                .add("XN", data1.get("XNDM").asString)
                .add("XQ", data1.get("XQDM").asString)
                .add("RQ", rqDateFormat.format(Date()))
                .build()
            val request2 = Request.Builder()
                .url("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do")
                .post(requestBody2)
                .build()
            val response2 = httpClient.newCall(request2).execute()
            val result2 = response2.body()?.string()
            val data2 = JsonParser.parseString(result2)
                .asJsonObject
                .getAsJsonObject("datas")
                .getAsJsonObject("cxrqdydzcxq")
                .getAsJsonArray("rows")
                .get(0)
                .asJsonObject
            timeInfo.ZC = data2.get("ZC").asString.toInt()
            timeInfo.ZZC = data2.get("ZZC").asString.toInt()

            val requestBody3 = FormBody.Builder()
                .add("XN", data1.get("XNDM").asString)
                .add("XQ", data1.get("XQDM").asString)
                .add("RQ", rqDateFormat.format(Date()))
                .build()
            val request3 = Request.Builder()
                .url("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do")
                .post(requestBody3)
                .build()
            val response3 = httpClient.newCall(request3).execute()
            val result3 = response3.body()?.string()
            val data3 = JsonParser.parseString(result3)
                .asJsonObject
                .getAsJsonObject("datas")
                .getAsJsonObject("cxxljc")
                .getAsJsonArray("rows")
                .get(0)
                .asJsonObject
            timeInfo.ZJXZC = data3.get("ZJXZC").asString.toInt()

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
            building.values.forEach { jasRecords ->
                jasRecords as MutableList
                jasRecords.sortBy { it.jasmc }
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

    open fun getClassInfo(classroom: JasRecord, timeInfo: TimeInfo): CompletableFuture<*> =
        CompletableFuture.supplyAsync {
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
                kcb[day].forEach { kcbItem ->
                    val jc = kcbItem.JC.split(',')
                    val kcbRecord = KcbRecord(
                        jxlmc = classroom.jxldmDisplay,
                        jsmph = classroom.jasmc?.replace(Regex("^${classroom.jxldmDisplay}"), "")?.trim(),
                        jasdm = classroom.jasdm,
                        skzws = classroom.skzws,
                        zylxdm = kcbItem.ZYLXDM.ifEmpty { "00" },
                        jcKs = jc.firstOrNull()?.toShort(),
                        jcJs = jc.lastOrNull()?.toShort(),
                        day = Weekday[day].value,
                        sfyxzx = classroom.sfyxzx,
                        jyytms = if (kcbItem.JYYTMS.isNullOrEmpty()) "" else kcbItem.JYYTMS,
                        kcm = kcbItem.KCM ?: if (kcbItem.KBID != null) "研究生课" else "未知",
                    )
                    kcbMapper.insert(kcbRecord)
                }
            }
        }

    private fun getKcb(xnxqdm: String, week: String, jasdm: String): MutableList<List<KcbItem>> {
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
        val by1 = JsonParser.parseString(result)
            .asJsonObject
            .getAsJsonObject("datas")
            .getAsJsonObject("cxyzjskjyqk")
            .getAsJsonArray("rows")
            .get(0)
            .asJsonObject
            .get("BY1")
            .asString
        return GsonUtil.fromJson(by1)
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
                    timetableMapper.delete {
                        where(TimetableDynamicSqlSupport.Timetable.day, isEqualTo(record.day))
                        and(TimetableDynamicSqlSupport.Timetable.jasdm, isEqualTo(record.jasdm))
                        and(TimetableDynamicSqlSupport.Timetable.jcKs, isEqualTo(jc.toShort()))
                        and(TimetableDynamicSqlSupport.Timetable.jcJs, isEqualTo(jc.toShort()))
                    }
            }
            timetableMapper.update {
                set(TimetableDynamicSqlSupport.Timetable.skzws).equalTo(record.skzws)
                set(TimetableDynamicSqlSupport.Timetable.zylxdm).equalTo(record.zylxdm)
                set(TimetableDynamicSqlSupport.Timetable.jyytms).equalTo(record.jyytms)
                set(TimetableDynamicSqlSupport.Timetable.kcm).equalTo(record.kcm)
                set(TimetableDynamicSqlSupport.Timetable.jcKs).equalTo(record.jcKs)
                where(TimetableDynamicSqlSupport.Timetable.day, isEqualTo(record.day))
                and(TimetableDynamicSqlSupport.Timetable.jasdm, isEqualTo(record.jasdm))
                and(TimetableDynamicSqlSupport.Timetable.jcKs, isEqualTo(record.jcJs))
                and(TimetableDynamicSqlSupport.Timetable.jcJs, isEqualTo(record.jcJs))
            }
        }
    }

    private fun mergeData() {
        val data = timetableMapper.select {
            orderBy(
                TimetableDynamicSqlSupport.Timetable.day,
                TimetableDynamicSqlSupport.Timetable.jxlmc,
                TimetableDynamicSqlSupport.Timetable.jsmph,
                TimetableDynamicSqlSupport.Timetable.jcJs,
            )
        }.groupBy {
            it.jxlmc!!
        }
        val result = mutableMapOf<String, MutableList<TimetableRecord>>()
        data.map { (jxlmc, records) ->
            mergeJxl(jxlmc, records, result)
        }.forEach { future -> future.join() }
        // 清空数据库
        timetableMapper.truncate()
        // 重新插入数据库
        val sqlSession = sqlSessionFactory.openSession(ExecutorType.BATCH, false)
        val timetableMapper = sqlSession.getMapper(TimetableMapper::class.java)
        result.forEach { (jxlmc, records) ->
            records.forEach { record ->
                timetableMapper.insert(record)
            }
            sqlSession.commit()
            logger.info("[{}] 归并完成.", jxlmc)
        }
        sqlSession.clearCache()
    }

    open fun mergeJxl(
        jxlmc: String,
        records: List<TimetableRecord>,
        result: MutableMap<String, MutableList<TimetableRecord>>
    ): CompletableFuture<*> = CompletableFuture.supplyAsync {
        logger.info("[{}] 开始归并...", jxlmc)
        val classrooms = mutableListOf<TimetableRecord>()
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

    override fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String): Boolean {
        val cookies = cookieService.getCookies()
        httpClient = cookieService.getHttpClient(cookies)
        val timeInfo = getTimeInfo()
        val kcb = getKcb(timeInfo.XNXQDM, timeInfo.ZC.toString(), jasdm)
        kcb[day.ordinal].forEach {
            val bool1 = jc.toString() in it.JC.split(',')
            val bool2 = it.ZYLXDM == zylxdm || it.ZYLXDM.isEmpty()
            if (bool1 && bool2) return true
        }
        return false
    }

    init {
        cacheService.flush()
    }
}