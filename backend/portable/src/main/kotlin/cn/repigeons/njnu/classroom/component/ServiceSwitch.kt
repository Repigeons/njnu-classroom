package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.service.RedisService
import org.springframework.stereotype.Component

@Component
class ServiceSwitch(
    private val redisService: RedisService
) {
    var value: Boolean
        set(value) = redisService.set("serviceSwitch", value)
        get() = redisService.get("serviceSwitch", Boolean::class.java) == true
}