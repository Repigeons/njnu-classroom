package cn.repigeons.njnu.classroom.service

import org.redisson.api.RLock
import org.redisson.api.RedissonClient
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import java.util.concurrent.TimeUnit

@Service
open class RedisService(
    private val redissonClient: RedissonClient
) {
    operator fun get(key: String) = this.get<String>(key)
    operator fun set(key: String, value: String) = this.set(key, value, null)

    @Transactional
    open fun delete(key: String) = redissonClient.getBucket<Any>(key).delete()

    @Transactional
    open fun <T> get(key: String, clazz: Class<T>? = null): T? = redissonClient.getBucket<T>(key).get()

    @Transactional
    open fun <T> set(key: String, value: T, expire: Long?) {
        val bucket = redissonClient.getBucket<T>(key)
        if (expire == null)
            bucket.set(value)
        else
            bucket.set(value, expire, TimeUnit.MILLISECONDS)
    }

    @Transactional
    open fun <T> getAndSet(key: String, value: T, expire: Long? = null): T? {
        val bucket = redissonClient.getBucket<T>(key)
        return if (expire == null)
            bucket.getAndSet(value)
        else
            bucket.getAndSet(value, expire, TimeUnit.SECONDS)
    }

    fun lock(name: String): RLock {
        val rLock = redissonClient.getLock(name)
        rLock.lock()
        return rLock
    }

    fun lock(name: String, time: Long, unit: TimeUnit): RLock {
        val rLock = redissonClient.getLock(name)
        rLock.lock(time, unit)
        return rLock
    }
}