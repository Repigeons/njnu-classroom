package cn.repigeons.njnu.classroom.service

interface CacheService {
    fun flushClassroomList()
    fun getClassroomList(): Map<String, *>

    fun flushBuildingPosition()
    fun getBuildingPosition(): List<*>
}