package cn.repigeons.njnu.classroom.configuration

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.http.client.BufferingClientHttpRequestFactory
import org.springframework.http.client.ClientHttpRequestFactory
import org.springframework.http.client.SimpleClientHttpRequestFactory
import org.springframework.http.converter.StringHttpMessageConverter
import org.springframework.web.client.RestTemplate
import java.nio.charset.StandardCharsets

@Configuration
open class RestTemplateConfiguration {
    @Bean
    open fun restTemplate(factory: ClientHttpRequestFactory): RestTemplate {
        val restTemplate = RestTemplate(factory)
        restTemplate.errorHandler = RestTemplateThrowErrorHandler()
        restTemplate.interceptors = listOf(RestTemplateRequestInterceptor())
        val messageConverters = restTemplate.messageConverters
        messageConverters[1] = StringHttpMessageConverter(StandardCharsets.UTF_8)
        messageConverters[2] = RestTemplateMessageConverter()
        return restTemplate
    }

    @Bean
    open fun simpleClientHttpRequestFactory(): ClientHttpRequestFactory {
        val factory = SimpleClientHttpRequestFactory()
        factory.setReadTimeout(120000)
        factory.setConnectTimeout(15000)
        return BufferingClientHttpRequestFactory(factory)
    }
}