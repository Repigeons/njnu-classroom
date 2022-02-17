package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.service.CacheService
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import kotlin.concurrent.thread

@Component
class ScheduledTask(
    private val cacheService: CacheService
) {
    init {
        thread {
            cacheService.flush()
            flushClassroomList()
        }
    }

    @Scheduled(cron = "0 0 9 * * *")
    fun flushClassroomList() = cacheService.flushClassroomList()
}