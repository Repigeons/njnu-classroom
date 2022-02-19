package cn.repigeons.njnu.classroom.service

interface CacheService {
    fun flush()

    fun flushClassroomList()
    fun getClassroomList(): Map<*, *>

    fun flushBuildingPosition()
    fun getBuildingPosition(): List<*>
}