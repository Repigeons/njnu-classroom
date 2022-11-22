package cn.repigeons.njnu.classroom.config

import cn.repigeons.commons.restTemplate.RestTemplateBuilder
import cn.repigeons.commons.restTemplate.build
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.web.client.RestTemplate
import java.time.Duration

@Configuration
open class RestTemplateConfig {
    @Bean
    open fun restTemplate(): RestTemplate =
        RestTemplateBuilder()
            .connectTimeout(Duration.ofSeconds(15))
            .readTimeout(Duration.ofSeconds(120))
            .build()
}
