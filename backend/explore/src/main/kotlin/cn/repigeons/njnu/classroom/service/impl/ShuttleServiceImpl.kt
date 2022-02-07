package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.service.MailService
import cn.repigeons.njnu.classroom.service.ShuttleService
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.io.File

@Service
open class ShuttleServiceImpl(
    private val mailService: MailService
) : ShuttleService {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Async
    override fun sendShuttleImage(file: MultipartFile) {
        logger.info("upload shuttle image: {}", file.originalFilename)
        val attachment = File.createTempFile(
            "shuttle_",
            ".${file.originalFilename?.split('.')?.lastOrNull()}"
        ).apply {
            file.transferTo(this)
            deleteOnExit()
        }
        logger.info("send shuttle image file: {}", attachment.name)
        mailService.send(
            subject = "【南师教室】有人上传校车时刻表.${file.originalFilename?.split('.')?.lastOrNull()}",
            content = "",
            attachment
        )
    }
}