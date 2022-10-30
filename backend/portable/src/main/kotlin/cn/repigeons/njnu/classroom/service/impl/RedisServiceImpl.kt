package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.util.GsonUtil
import io.netty.buffer.ByteBufAllocator
import io.netty.buffer.ByteBufInputStream
import io.netty.buffer.ByteBufOutputStream
import org.redisson.api.RedissonClient
import org.redisson.client.codec.BaseCodec
import org.redisson.client.codec.StringCodec
import org.redisson.client.protocol.Decoder
import org.redisson.client.protocol.Encoder
import org.springframework.stereotype.Service
import java.time.Duration
import java.util.concurrent.TimeUnit

@Service
open class RedisServiceImpl(
    private val redissonClient: RedissonClient
) : RedisService {
    override fun <T> set(key: String, value: T) = this.set(key, value, null)
    override fun <T> get(key: String) = this.get(key, Any::class.java) as T?

    override fun <T> set(key: String, value: T, expire: Long?) {
        val bucket = redissonClient.getBucket<T>(key, codec)
        if (expire == null)
            bucket.set(value)
        else
            bucket.set(value, expire, TimeUnit.SECONDS)
    }

    override fun <T> get(key: String, clazz: Class<T>): T? {
        return redissonClient.getBucket<T>(key, codec).get()
    }

    override fun del(key: String): Boolean {
        return redissonClient.getBucket<Any>(key, codec).delete()
    }

    override fun hasKey(key: String): Boolean {
        return redissonClient.getBucket<Any>(key, codec).isExists
    }

    override fun <T> hSet(key: String, field: String, value: T): T? {
        val map = redissonClient.getMap<String, T>(key, codec)
        return map.put(field, value)
    }

    override fun <T> hGet(key: String, field: String): T? {
        val map = redissonClient.getMap<String, T>(key, codec)
        return map[field]
    }

    override fun <T> hKeys(key: String): Set<String> {
        val map = redissonClient.getMap<String, T>(key, codec)
        return map.keys
    }

    override fun <T> hGetAll(key: String): MutableMap<String, T> {
        val map = redissonClient.getMap<String, T>(key, codec)
        return map.readAllMap()
    }

    override fun <T> hSet(key: String, values: Map<String, T>) {
        val map = redissonClient.getMap<String, T>(key, codec)
        return map.putAll(values)
    }

    override fun hDel(key: String, field: String): Boolean {
        val map = redissonClient.getMap<String, Any>(key, codec)
        return map.remove(field) != null
    }

    override fun expire(key: String, expire: Long): Boolean {
        val bucket = redissonClient.getBucket<Any>(key, codec)
        return bucket.expire(Duration.ofSeconds(expire))
    }

    private val codec = object : BaseCodec() {
        private val TYPE = "@type"
        private val DATA = "@data"
        private val valueEncoder = Encoder { input ->
            try {
                val data = mapOf(
                    Pair(TYPE, input.javaClass.name),
                    Pair(DATA, GsonUtil.toJson(input))
                )
                ByteBufOutputStream(ByteBufAllocator.DEFAULT.buffer()).use { outputStream ->
                    outputStream.write(GsonUtil.toJson(data).encodeToByteArray())
                    outputStream.buffer()
                }
            } catch (e: Exception) {
                null
            }
        }
        private val valueDecoder = Decoder { byteBuf, _ ->
            try {
                val data: Map<String, String> = ByteBufInputStream(byteBuf).use { reader ->
                    GsonUtil.fromJson(reader.reader())
                }
                val clazz = Class.forName(data[TYPE] as String)
                GsonUtil.gson.fromJson(data[DATA], clazz)
            } catch (e: Exception) {
                null
            }
        }
        private val codec = StringCodec()
        override fun getValueEncoder() = valueEncoder
        override fun getValueDecoder() = valueDecoder
        override fun getMapKeyEncoder(): Encoder = codec.mapKeyEncoder
        override fun getMapKeyDecoder(): Decoder<Any> = codec.mapKeyDecoder
        override fun getMapValueEncoder() = valueEncoder
        override fun getMapValueDecoder() = valueDecoder
    }
}