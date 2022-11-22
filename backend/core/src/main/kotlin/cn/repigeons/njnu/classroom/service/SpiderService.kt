package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.enumerate.Weekday
import org.springframework.cloud.openfeign.FeignClient
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestParam

@FeignClient(
    name = "SpiderService",
    url = "http://spider:8080",
    path = "spider",
    fallback = SpiderServiceFallback::class
)
interface SpiderService {
    @PostMapping("/run")
    fun run()

    @PostMapping("/checkWithEhall")
    fun checkWithEhall(
        @RequestParam jasdm: String,
        @RequestParam weekday: Weekday,
        @RequestParam jc: Short,
        @RequestParam zylxdm: String
    ): Boolean

    @PostMapping("/flush")
    fun flushCache()
}

class SpiderServiceFallback : SpiderService {
    override fun run() {}
    override fun checkWithEhall(jasdm: String, weekday: Weekday, jc: Short, zylxdm: String) = true
    override fun flushCache() {}
}