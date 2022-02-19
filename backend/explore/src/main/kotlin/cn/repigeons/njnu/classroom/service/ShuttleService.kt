package cn.repigeons.njnu.classroom.service

import org.springframework.web.multipart.MultipartFile

interface ShuttleService {
    fun flushRoute()
    fun sendShuttleImage(file: MultipartFile)

    fun flushStationPosition()
    fun getStationPosition(): List<*>
}