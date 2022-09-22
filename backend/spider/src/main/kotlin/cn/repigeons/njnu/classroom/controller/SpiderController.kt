package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.SpiderService
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("spider")
class SpiderController(
    private val spiderService: SpiderService,
    private val cacheService: CacheService
) {
    @PostMapping("run")
    fun runSpider(): JsonResponse {
        spiderService.run()
        return JsonResponse(status = Status.ACCEPTED)
    }

    @PostMapping("flush")
    fun flushCache(): JsonResponse {
        cacheService.flush()
        return JsonResponse(status = Status.ACCEPTED)
    }
}