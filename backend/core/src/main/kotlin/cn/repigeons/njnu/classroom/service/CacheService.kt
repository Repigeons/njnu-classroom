package cn.repigeons.njnu.classroom.service

import java.util.concurrent.Future

interface CacheService {
    fun flush(): Future<*>

    fun flushClassroomList()
    fun getClassroomList(): Map<String, *>
}