package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.commons.redisTemplate.RedisService
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.model.EmptyClassroom
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.CacheService
import org.mybatis.dynamic.sql.util.kotlin.elements.isIn
import org.redisson.api.RedissonClient
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service
import java.util.concurrent.CompletableFuture

@Service
class CacheServiceImpl(
    private val redisService: RedisService,
    private val redissonClient: RedissonClient,
    private val timetableMapper: TimetableMapper
) : CacheService {
    private val logger = LoggerFactory.getLogger(javaClass)

    override fun flush(): CompletableFuture<*> = CompletableFuture.supplyAsync {
        val lock = redissonClient.getLock("lock:flush")
        if (!lock.tryLock()) {
            logger.info("刷新缓存数据已处于运行中...")
            return@supplyAsync
        }
        try {
            logger.info("开始刷新缓存数据...")
            val startTime = System.currentTimeMillis()
            val t1 = flushEmptyClassrooms()
            val t2 = flushOverview()
            t1.join(); t2.join()
            val endTime = System.currentTimeMillis()
            logger.info("缓存刷新完成. 共计耗时 {} 秒", (endTime - startTime) / 1000)
        } finally {
            lock.unlock()
        }
    }

    private fun flushEmptyClassrooms(): CompletableFuture<*> = CompletableFuture.supplyAsync {
        redisService.del("empty")
        logger.info("开始刷新空教室缓存...")
        val map = timetableMapper.select {
            where(TimetableDynamicSqlSupport.Timetable.zylxdm, isIn("00", "10", "11"))
        }
            .groupBy {
                "${it.jxlmc}:${it.weekday}"
            }
            .map { (key, records) ->
                logger.debug("Flushing empty classroom: {}", key)
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
                key to value
            }
            .toTypedArray()
            .let { mapOf(*it) }
        redisService.hSetAll("empty", map)
        logger.info("空教室缓存刷新完成")
    }

    private fun flushOverview(): CompletableFuture<*> = CompletableFuture.supplyAsync {
        redisService.del("overview")
        logger.info("开始刷新教室概览缓存...")
        val map = timetableMapper.select {}
            .groupBy {
                it.jasdm!!
            }
            .map { (key, records) ->
                val classroomName = records.firstOrNull()?.let { it.jxlmc + it.jsmph }
                logger.debug("Flushing overview: {}", classroomName)
                val value = records.map { QueryResultItem(it) }
                Pair(key, value)
            }
            .toTypedArray()
            .let { mapOf(*it) }
        redisService.hSetAll("overview", map)
        logger.info("教室概览缓存刷新完成")
    }
}