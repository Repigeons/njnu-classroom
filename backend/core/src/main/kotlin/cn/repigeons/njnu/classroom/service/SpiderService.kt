package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.Weekday
import org.springframework.cloud.openfeign.FeignClient
import org.springframework.web.bind.annotation.GetMapping

@FeignClient(
    name = "SpiderService",
    url = "http://spider:8080",
    fallback = SpiderServiceFallback::class
)
interface SpiderService {
    @GetMapping("/run")
    fun run()

    @GetMapping("/checkWithEhall")
    fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String): Boolean

    @GetMapping("/flushCache")
    fun flushCache()
}

class SpiderServiceFallback : SpiderService {
    override fun run() {}
    override fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String) = true
    override fun flushCache() {}
}