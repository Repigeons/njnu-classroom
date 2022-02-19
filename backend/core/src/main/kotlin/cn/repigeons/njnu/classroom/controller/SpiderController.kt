package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.component.ServiceSwitch
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.SpiderService
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("spider")
class SpiderController(
    private val serviceSwitch: ServiceSwitch,
    private val spiderService: SpiderService,
    private val cacheService: CacheService
) {
    @PostMapping("run")
    fun runSpider(): JsonResponse {
        if (!serviceSwitch.value) {
            return JsonResponse(
                status = Status.IM_A_TEAPOT,
                message = "service off"
            )
        }
        spiderService.run()
        return JsonResponse(status = Status.ACCEPTED)
    }

    @PostMapping("flush")
    fun flushCache(): JsonResponse {
        if (!serviceSwitch.value) {
            return JsonResponse(
                status = Status.IM_A_TEAPOT,
                message = "service off"
            )
        }
        cacheService.flush()
        return JsonResponse(status = Status.ACCEPTED)
    }
}