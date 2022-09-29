package cn.repigeons.njnu.classroom.util

import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.Reader

object GsonUtil {
    private val gson = GsonBuilder().serializeNulls().enableComplexMapKeySerialization().disableHtmlEscaping().create()
    fun toJson(src: Any): String = gson.toJson(src)
    fun <T> fromJson(reader: Reader): T = gson.fromJson(reader, object : TypeToken<T>() {}.type)
    fun <T> fromJson(json: String): T = gson.fromJson(json, object : TypeToken<T>() {}.type)
    fun <T> fromJson(json: String, classOfT: Class<T>): T = fromJson(json)
    fun <T> reload(src: Any): T = fromJson(toJson(src))
    fun <T> reload(src: Any, classOfT: Class<T>): T = fromJson(toJson(src))
}