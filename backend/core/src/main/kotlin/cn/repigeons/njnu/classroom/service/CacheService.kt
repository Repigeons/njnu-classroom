package cn.repigeons.njnu.classroom.service

import org.redisson.api.RLock
import java.util.concurrent.Future

interface CacheService {
    fun flush(lock: RLock? = null): Future<*>

    fun flushClassroomList()
    fun getClassroomList(): Map<String, *>
}