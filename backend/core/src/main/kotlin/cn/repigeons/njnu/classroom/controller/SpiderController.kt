package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.SpiderService
import org.redisson.api.RedissonClient
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import java.util.concurrent.TimeUnit

@RestController
@RequestMapping("spider")
class SpiderController(
    private val redissonClient: RedissonClient,
    private val spiderService: SpiderService,
    private val cacheService: CacheService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Scheduled(cron = "0 0 8 * * *")
    @PostMapping("run")
    fun runSpider(): JsonResponse {
        val rLock = redissonClient.getLock("spider")
        try {
            if (!rLock.tryLock(60, TimeUnit.MINUTES))
                return JsonResponse()

            logger.info("开始课程信息收集工作...")
            spiderService.run(rLock)
        } catch (e: Exception) {
            rLock.unlock()
            throw e
        }
        return JsonResponse(status = Status.ACCEPTED)
    }

    @PostMapping("flush")
    fun flushCache(): JsonResponse {
        val rLock = redissonClient.getLock("flush")
        try {
            if (!rLock.tryLock(5, TimeUnit.MINUTES))
                return JsonResponse()
            logger.info("开始刷新缓存数据...")
            cacheService.flush(rLock)
        } catch (e: Exception) {
            rLock.unlock()
            throw e
        }
        return JsonResponse(status = Status.ACCEPTED)
    }
}