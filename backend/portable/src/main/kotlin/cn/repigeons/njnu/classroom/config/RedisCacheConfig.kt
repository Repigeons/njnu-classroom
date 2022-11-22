package cn.repigeons.njnu.classroom.config

import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Primary
import org.springframework.data.redis.cache.RedisCacheConfiguration
import org.springframework.data.redis.cache.RedisCacheManager
import org.springframework.data.redis.connection.RedisConnectionFactory
import org.springframework.data.redis.core.RedisTemplate
import org.springframework.data.redis.serializer.RedisSerializationContext
import java.time.Duration

@Configuration
open class RedisCacheConfig(
    private val redisTemplate: RedisTemplate<String, Any>,
    @Value("\${redis.key-prefix:}")
    private val REDIS_KEY_PREFIX: String,
    @Value("\${spring.cache.redis.key-prefix:}")
    private val SPRING_CACHE_KEY_PREFIX: String
) {
    @Bean
    @Primary
    open fun cacheManagerOf1d(connectionFactory: RedisConnectionFactory) =
        RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(cacheConfiguration(ttl = Duration.ofDays(1)))
            .build()

    private fun cacheConfiguration(ttl: Duration) =
        RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(ttl)
            .disableCachingNullValues()
            .prefixCacheNameWith("$REDIS_KEY_PREFIX:$SPRING_CACHE_KEY_PREFIX")
            .serializeKeysWith(RedisSerializationContext.SerializationPair.fromSerializer(redisTemplate.stringSerializer))
            .serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(redisTemplate.valueSerializer))

}