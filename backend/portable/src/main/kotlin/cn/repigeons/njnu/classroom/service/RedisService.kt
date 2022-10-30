package cn.repigeons.njnu.classroom.service

interface RedisService {
    operator fun <T> set(key: String, value: T)
    operator fun <T> get(key: String): T?

    // String
    fun <T> set(key: String, value: T, expire: Long? = null)
    fun <T> get(key: String, clazz: Class<T>): T?
    fun del(key: String): Boolean
    fun hasKey(key: String): Boolean

    // Hash
    fun <T> hSet(key: String, field: String, value: T): T?
    fun <T> hGet(key: String, field: String): T?
    fun <T> hKeys(key: String): Set<String>
    fun <T> hGetAll(key: String): MutableMap<String, T>
    fun <T> hSet(key: String, values: Map<String, T>)
    fun hDel(key: String, field: String): Boolean

    // List

    // Set

    //
    fun expire(key: String, expire: Long): Boolean
}