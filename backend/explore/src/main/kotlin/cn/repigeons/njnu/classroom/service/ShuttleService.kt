package cn.repigeons.njnu.classroom.service

import java.util.concurrent.Future

interface ShuttleService {
    fun flushRoute(): Future<*>
    fun sendShuttleImage(filename: String?, bytes: ByteArray): Future<*>

    fun flushStationPosition(): Future<*>
    fun getStationPosition(): List<*>
}