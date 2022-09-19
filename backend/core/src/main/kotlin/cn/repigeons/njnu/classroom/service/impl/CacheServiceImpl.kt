package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.model.EmptyClassroom
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.util.GsonUtil
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.redisson.api.RedissonClient
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.scheduling.annotation.Async
import org.springframework.scheduling.annotation.AsyncResult
import org.springframework.stereotype.Service
import org.springframework.util.concurrent.ListenableFuture
import java.util.*
import java.util.concurrent.TimeUnit

@Service
open class CacheServiceImpl(
    private val redissonClient: RedissonClient,
    private val redisService: RedisService,
    private val jasMapper: JasMapper,
    private val devMapper: DevMapper,
    private val proMapper: ProMapper,
    private val positionsMapper: PositionsMapper,
    @Value("\${spring.profiles.active}")
    private val env: String
) : CacheService {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Async
    override fun flush() {
        val lock = redissonClient.getLock("lock:flush")
        if (lock.tryLock(1, 60 * 60, TimeUnit.SECONDS)) {
            logger.info("刷新缓存数据已处于运行中...")
            return
        }
        try {
            logger.info("开始刷新缓存数据...")
            this.actFlush()
        } finally {
            lock.unlock()
        }
    }

    private fun actFlush() {
        val startTime = Date()
        val t1 = flushEmptyClassrooms().completable()
        val t2 = flushOverview().completable()
        t1.join()
        t2.join()

        val endTime = Date()
        logger.info("缓存刷新完成. 共计耗时 {} 秒", (endTime.time - startTime.time) / 1000)
    }

    @Async
    open fun flushEmptyClassrooms(): ListenableFuture<*> {
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
                    rMap[key] = GsonUtil.toJson(value)
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
                    rMap[key] = GsonUtil.toJson(value)
                }
        }
        logger.info("Flush empty classroom completed.")
        return AsyncResult(null)
    }

    @Async
    open fun flushOverview(): ListenableFuture<*> {
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
                    rMap[key] = GsonUtil.toJson(value)
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
                    rMap[key] = GsonUtil.toJson(value)
                }
        }
        logger.info("Flush overview completed.")
        return AsyncResult(null)
    }

    @Async
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
        redisService["static:classrooms"] = GsonUtil.toJson(classrooms)
    }

    override fun getClassroomList(): Map<*, *> = GsonUtil.fromJson(
        redisService["static:classrooms"]!!, Map::class.java
    )

    @Async
    override fun flushBuildingPosition() {
        val positions = positionsMapper.select {
            where(PositionsDynamicSqlSupport.Positions.kind, isEqualTo(1))
        }.map {
            mapOf(
                Pair("name", it.name),
                Pair("position", listOf(it.latitude, it.longitude))
            )
        }
        redisService["static:position:building"] = GsonUtil.toJson(positions)
    }

    override fun getBuildingPosition(): List<*> = GsonUtil.fromJson(
        redisService["static:position:building"]!!, List::class.java
    )
}