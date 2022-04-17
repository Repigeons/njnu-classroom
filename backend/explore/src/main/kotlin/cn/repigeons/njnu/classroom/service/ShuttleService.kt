package cn.repigeons.njnu.classroom.service

interface ShuttleService {
    fun flushRoute()
    fun sendShuttleImage(filename: String?, bytes: ByteArray)

    fun flushStationPosition()
    fun getStationPosition(): List<*>
}