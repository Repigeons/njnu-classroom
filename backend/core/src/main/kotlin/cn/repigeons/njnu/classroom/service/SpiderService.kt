package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.Weekday
import org.springframework.cloud.openfeign.FeignClient
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam

@FeignClient(
    name = "SpiderService",
    url = "http://spider:8080",
    path = "spider",
    fallback = SpiderServiceFallback::class
)
interface SpiderService {
    @GetMapping("/run")
    fun run()

    @GetMapping("/checkWithEhall")
    fun checkWithEhall(
        @RequestParam jasdm: String,
        @RequestParam day: Weekday,
        @RequestParam jc: Short,
        @RequestParam zylxdm: String
    ): Boolean

    @GetMapping("/flushCache")
    fun flushCache()
}

class SpiderServiceFallback : SpiderService {
    override fun run() {}
    override fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String) = true
    override fun flushCache() {}
}