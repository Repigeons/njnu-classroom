package cn.repigeons.njnu.classroom.configuration

import org.redisson.Redisson
import org.redisson.api.RedissonClient
import org.redisson.codec.JsonJacksonCodec
import org.redisson.config.Config
import org.redisson.config.TransportMode
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
open class RedissonConfiguration(
    @Value("\${spring.redis.host:127.0.0.1}")
    private val host: String,
    @Value("\${spring.redis.port:6379}")
    private val port: Int,
    @Value("\${spring.redis.database:0}")
    private val database: Int,
    @Value("\${spring.redis.username:#{null}}")
    private val username: String?,
    @Value("\${spring.redis.password:#{null}}")
    private val password: String?,
) {
    @Bean
    open fun redissonClient(): RedissonClient {
        val config = Config().apply {
            val config = useSingleServer()
            config.address = "redis://$host:$port"
            config.database = database
            config.username = username
            config.password = password
            config.connectionMinimumIdleSize = 8
            transportMode = TransportMode.NIO
            codec = JsonJacksonCodec()
        }
        return Redisson.create(config)
    }
}