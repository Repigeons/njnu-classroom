package cn.repigeons.njnu.classroom.config

import cn.repigeons.commons.redisTemplate.RedisService
import cn.repigeons.commons.redisTemplate.RedisServiceBuilder
import cn.repigeons.commons.redisTemplate.RedisTemplateBuilder
import cn.repigeons.commons.redisTemplate.build
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.data.redis.connection.RedisConnectionFactory
import org.springframework.data.redis.core.RedisTemplate

@Configuration
open class RedisConfig {
    @Bean
    open fun redisTemplate(redisConnectionFactory: RedisConnectionFactory): RedisTemplate<String, Any> =
        RedisTemplateBuilder<Any>()
            .redisConnectionFactory(redisConnectionFactory)
            .build()

    @Bean
    open fun redisService(redisTemplate: RedisTemplate<String, Any>): RedisService =
        RedisServiceBuilder()
            .redisTemplate(redisTemplate)
            .build()
}
