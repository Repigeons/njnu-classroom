package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.service.SpiderService
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component

@Component
class ScheduledTask(
    private val spiderService: SpiderService,
) {
    @Scheduled(cron = "0 0 8 * * *")
    fun runSpider() {
        spiderService.run()
    }
}