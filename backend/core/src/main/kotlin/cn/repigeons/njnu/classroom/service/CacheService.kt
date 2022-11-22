package cn.repigeons.njnu.classroom.service

import java.util.concurrent.Future

interface CacheService {
    fun flushClassroomList(): Future<*>
    fun getClassroomList(): Map<*, *>

    fun flushBuildingPosition(): Future<*>
    fun getBuildingPosition(): List<*>
}