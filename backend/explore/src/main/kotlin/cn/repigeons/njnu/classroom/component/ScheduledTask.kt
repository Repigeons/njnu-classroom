package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.service.ShuttleService
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import kotlin.concurrent.thread

@Component
class ScheduledTask(
    private val shuttleService: ShuttleService
) {
    init {
        thread {
            flushShuttleLine()
        }
    }

    @Scheduled(cron = "0 0 7 * * *")
    fun flushShuttleLine() = shuttleService.flush()
}