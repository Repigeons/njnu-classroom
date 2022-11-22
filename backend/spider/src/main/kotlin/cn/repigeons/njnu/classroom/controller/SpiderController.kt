package cn.repigeons.njnu.classroom.controller

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.njnu.classroom.enumerate.Weekday
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.SpiderService
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("spider")
class SpiderController(
    private val spiderService: SpiderService,
    private val cacheService: CacheService
) {
    @PostMapping("run")
    fun runSpider(): CommonResponse<*> {
        spiderService.run()
        return CommonResponse.success()
    }

    @PostMapping("flush")
    fun flushCache(): CommonResponse<*> {
        cacheService.flush()
        return CommonResponse.success()
    }

    @PostMapping("/checkWithEhall")
    fun checkWithEhall(
        @RequestParam jasdm: String,
        @RequestParam weekday: Weekday,
        @RequestParam jc: Short,
        @RequestParam zylxdm: String
    ): Boolean {
        return spiderService.checkWithEhall(jasdm, weekday, jc, zylxdm)
    }
}