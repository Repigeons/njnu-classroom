package cn.repigeons.njnu.classroom.service

import org.springframework.web.multipart.MultipartFile
import java.util.concurrent.Future

interface ShuttleService {
    fun flush(): Future<Void>
    fun sendShuttleImage(file: MultipartFile)
}