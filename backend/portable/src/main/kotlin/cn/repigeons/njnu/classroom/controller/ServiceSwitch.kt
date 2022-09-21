package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.service.RedisService
import org.slf4j.LoggerFactory
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class ServiceSwitch(
    private val redisService: RedisService
) {
    private val logger = LoggerFactory.getLogger(javaClass)
    var value: Boolean
        private set(value) = redisService.set("serviceSwitch", value)
        get() = redisService.get("serviceSwitch", Boolean::class.java) == true

    @PostMapping("switch")
    fun switch(value: Boolean?): JsonResponse {
        this.value = value ?: !this.value
        val message = if (this.value) "service on" else "service off"
        logger.info(message)
        return JsonResponse(
            message = message,
            data = message
        )
    }
}