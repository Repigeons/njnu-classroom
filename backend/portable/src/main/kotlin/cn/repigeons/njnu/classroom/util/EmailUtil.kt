package cn.repigeons.njnu.classroom.util

import cn.repigeons.njnu.classroom.component.SpringContextHolder
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Configuration
import org.springframework.mail.javamail.JavaMailSender
import org.springframework.mail.javamail.JavaMailSenderImpl
import org.springframework.mail.javamail.MimeMessageHelper
import java.io.File
import java.util.*

@Configuration
private open class EmailConfig {
    @Value("\${spring.mail.host:}")
    private var host = ""

    @Value("\${spring.mail.port:}")
    private var port = 0

    @Value("\${spring.mail.username:}")
    var username = ""
        private set

    @Value("\${spring.mail.password:}")
    private var password = ""

    @Value("\${spring.mail.default-encoding:UTF-8")
    private var defaultEncoding = "UTF-8"

    private val javaMailProperties = Properties().apply {
        this["mail.smtp.ssl.enable"] = "true"
    }

    val javaMailSender: JavaMailSender = JavaMailSenderImpl().apply {
        this.host = this@EmailConfig.host
        this.port = this@EmailConfig.port
        this.username = this@EmailConfig.username
        this.password = this@EmailConfig.password
        this.defaultEncoding = this@EmailConfig.defaultEncoding
        this.javaMailProperties = this@EmailConfig.javaMailProperties
    }
}

object EmailUtil {
    private val logger = LoggerFactory.getLogger(javaClass)
    private val emailConfig: EmailConfig = SpringContextHolder.getBean()
    private val mailSender = emailConfig.javaMailSender

    /**
     * 发送邮件
     */
    fun send(
        nickname: String? = null,
        subject: String,
        content: String,
        receivers: Array<String>,
        ccReceivers: Array<String>? = null,
        html: Boolean = false
    ) {
        logger.info("发送邮件：{},{},{},{}", subject, content, receivers, ccReceivers)
        val mimeMessage = mailSender.createMimeMessage()
        val helper = MimeMessageHelper(mimeMessage, false)
        // 发件人
        if (nickname == null)
            helper.setFrom(emailConfig.username)
        else
            helper.setFrom(emailConfig.username, nickname)
        // 收件人
        helper.setTo(receivers)
        // 抄送
        if (!ccReceivers.isNullOrEmpty())
            helper.setCc(ccReceivers)
        // 邮件主题
        helper.setSubject(subject)
        // 邮件内容
        helper.setText(content, html)
        mailSender.send(mimeMessage)
        logger.info("发送邮件成功")
    }

    /**
     * 附件邮件
     */
    fun sendFile(
        nickname: String? = null,
        subject: String,
        content: String,
        receivers: Array<String>,
        vararg attachments: File
    ) {
        logger.info("发送邮件：{},{},{},{}", subject, content, receivers, attachments)
        val mimeMessage = mailSender.createMimeMessage()
        val helper = MimeMessageHelper(mimeMessage, true)
        // 发件人
        if (nickname == null)
            helper.setFrom(emailConfig.username)
        else
            helper.setFrom(emailConfig.username, nickname)
        // 收件人
        helper.setTo(receivers)
        // 邮件主题
        helper.setSubject(subject)
        // 邮件内容
        helper.setText(content, true)
        attachments.forEach { file ->
            helper.addAttachment(file.name, file)
        }
        mailSender.send(mimeMessage)
        logger.info("发送邮件成功")
    }
}