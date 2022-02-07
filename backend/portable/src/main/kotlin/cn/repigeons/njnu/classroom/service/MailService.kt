package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.configuration.MailConfiguration
import org.springframework.mail.SimpleMailMessage
import org.springframework.mail.javamail.JavaMailSender
import org.springframework.mail.javamail.MimeMessageHelper
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service
import java.io.File

@Service
open class MailService(
    private val mailSender: JavaMailSender,
    private val mailConfiguration: MailConfiguration
) {
    @Async
    open fun sendPlain(
        subject: String,
        content: String,
    ) {
        val simpleMailMessage = SimpleMailMessage()
        // 发件人
        simpleMailMessage.from = mailConfiguration.sender
        // 收件人
        simpleMailMessage.setTo(*mailConfiguration.receivers.toTypedArray())
        // 邮件主题
        simpleMailMessage.subject = subject
        // 邮件内容
        simpleMailMessage.text = content
        mailSender.send(simpleMailMessage)
    }

    @Async
    open fun send(
        subject: String,
        content: String,
        vararg attachments: File,
    ) {
        val mimeMessage = mailSender.createMimeMessage()
        val helper = MimeMessageHelper(mimeMessage, true)
        // 发件人
        helper.setFrom(mailConfiguration.sender)
        // 收件人
        helper.setTo(mailConfiguration.receivers.toTypedArray())
        // 邮件主题
        helper.setSubject(subject)
        // 邮件内容
        helper.setText(content, true)
        attachments.forEach { file ->
            helper.addAttachment(file.name, file)
        }
        mailSender.send(mimeMessage)
    }
}