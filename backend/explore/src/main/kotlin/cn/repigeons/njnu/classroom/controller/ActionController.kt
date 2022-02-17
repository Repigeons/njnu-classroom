package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.component.ServiceSwitch
import org.slf4j.LoggerFactory
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("explore")
class ActionController(
    private val serviceSwitch: ServiceSwitch
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @PostMapping("switch")
    fun switch(value: Boolean?): JsonResponse {
        serviceSwitch.value = value ?: !serviceSwitch.value
        val message = if (serviceSwitch.value) "service on" else "service off"
        logger.info(message)
        return JsonResponse(
            message = message,
            data = message
        )
    }
}