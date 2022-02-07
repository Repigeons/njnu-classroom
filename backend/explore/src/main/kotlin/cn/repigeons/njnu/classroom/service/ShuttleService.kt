package cn.repigeons.njnu.classroom.service

import org.springframework.web.multipart.MultipartFile

interface ShuttleService {
    fun sendShuttleImage(file: MultipartFile)
}