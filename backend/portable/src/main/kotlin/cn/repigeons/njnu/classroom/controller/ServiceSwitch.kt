package cn.repigeons.njnu.classroom.controller

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.commons.redisTemplate.RedisService
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
        get() = redisService["serviceSwitch"] == true

    @PostMapping("switch")
    fun switch(value: Boolean?): CommonResponse<*> {
        this.value = value ?: !this.value
        val message = if (this.value) "service on" else "service off"
        logger.info(message)
        return CommonResponse.success(
            message = message,
            data = message
        )
    }
}