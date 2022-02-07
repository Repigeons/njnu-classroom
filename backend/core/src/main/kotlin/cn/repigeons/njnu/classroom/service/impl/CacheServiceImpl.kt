package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.mbg.mapper.DevMapper
import cn.repigeons.njnu.classroom.mbg.mapper.JasMapper
import cn.repigeons.njnu.classroom.mbg.mapper.ProMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.model.EmptyClassroom
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.RedisService
import com.google.gson.Gson
import org.redisson.api.RLock
import org.redisson.api.RedissonClient
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.scheduling.annotation.Async
import org.springframework.scheduling.annotation.AsyncResult
import org.springframework.stereotype.Service
import java.util.*
import java.util.concurrent.Future
import kotlin.concurrent.thread

@Service
open class CacheServiceImpl(
    private val gson: Gson,
    private val redissonClient: RedissonClient,
    private val redisService: RedisService,
    private val jasMapper: JasMapper,
    private val devMapper: DevMapper,
    private val proMapper: ProMapper,
    @Value("env") private val env: String
) : CacheService {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Async
    override fun flush(lock: RLock?): Future<Void> {
        val startTime = Date()

        val t1 = thread { flushEmptyClassrooms() }
        val t2 = thread { flushOverview() }
        t1.join()
        t2.join()

        val endTime = Date()
        logger.info("缓存刷新完成. 共计耗时 {} 秒", (endTime.time - startTime.time) / 1000)
        lock?.unlock()
        return AsyncResult(null)
    }

    private fun flushEmptyClassrooms() {
        val rMap = redissonClient.getMap<String, String>("empty")
        rMap.delete()
        if (env == "pro") {
            devMapper.select {}
                .groupBy {
                    "${it.jxlmc}:${it.day}"
                }
                .forEach { (key, records) ->
                    logger.info("Flushing empty classroom: {}", key)
                    val value = records.map { record ->
                        val item = EmptyClassroom()
                        item.jasdm = record.jasdm!!
                        item.jsmph = record.jsmph!!
                        item.skzws = record.skzws!!
                        item.jcKs = record.jcKs!!
                        item.jcJs = record.jcJs!!
                        item.zylxdm = record.zylxdm!!
                        item
                    }
                    rMap[key] = gson.toJson(value)
                }
        } else {
            proMapper.select {}
                .groupBy {
                    "${it.jxlmc}:${it.day}"
                }
                .forEach { (key, records) ->
                    logger.info("Flushing empty classroom: {}", key)
                    val value = records.map { record ->
                        val item = EmptyClassroom()
                        item.jasdm = record.jasdm!!
                        item.jsmph = record.jsmph!!
                        item.skzws = record.skzws!!
                        item.jcKs = record.jcKs!!
                        item.jcJs = record.jcJs!!
                        item.zylxdm = record.zylxdm!!
                        item
                    }
                    rMap[key] = gson.toJson(value)
                }
        }
        logger.info("Flush empty classroom completed.")
    }

    private fun flushOverview() {
        val rMap = redissonClient.getMap<String, String>("overview")
        rMap.delete()
        if (env == "pro") {
            devMapper.select {}
                .groupBy {
                    it.jasdm!!
                }
                .forEach { (key, records) ->
                    val classroomName = records.firstOrNull()?.let { it.jxlmc + it.jsmph }
                    logger.info("Flushing overview: {}", classroomName)
                    val value = records.map { QueryResultItem(it) }
                    rMap[key] = gson.toJson(value)
                }
        } else {
            proMapper.select {}
                .groupBy {
                    it.jasdm!!
                }
                .forEach { (key, records) ->
                    val classroomName = records.firstOrNull()?.let { it.jxlmc + it.jsmph }
                    logger.info("Flushing overview: {}", classroomName)
                    val value = records.map { QueryResultItem(it) }
                    rMap[key] = gson.toJson(value)
                }
        }
        logger.info("Flush overview completed.")
    }

    override fun flushClassroomList() {
        val classrooms = jasMapper.select {}
            .map {
                mapOf(
                    Pair("jxlmc", it.jxldmDisplay),
                    Pair("jsmph", it.jasmc?.replace(Regex("^${it.jxldmDisplay}"), "")?.trim()),
                    Pair("jasdm", it.jasdm)
                )
            }
            .groupBy { it["jxlmc"]!! }
        redisService["static:classrooms"] = gson.toJson(classrooms)
    }

    override fun getClassroomList(): Map<String, *> = gson.fromJson<Map<String, *>>(
        redisService["static:classrooms"], Map::class.java
    )
}