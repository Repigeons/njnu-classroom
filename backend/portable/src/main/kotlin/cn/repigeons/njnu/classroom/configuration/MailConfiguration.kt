package cn.repigeons.njnu.classroom.configuration

import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.context.annotation.Configuration

@Configuration
@ConfigurationProperties(prefix = "spring.mail")
open class MailConfiguration(
    val receivers: ArrayList<String>,
    @Value("\${spring.mail.username}") val sender: String
)