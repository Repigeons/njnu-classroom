package cn.repigeons.njnu.classroom.util

import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.Reader
import java.lang.reflect.Type

object GsonUtil {
    private val gson = GsonBuilder().serializeNulls().enableComplexMapKeySerialization().disableHtmlEscaping().create()
    inline fun <reified T> fromJson(json: String): T = fromJson(json, object : TypeToken<T>() {}.type)
    fun <T> fromJson(json: String, classOfT: Type): T = gson.fromJson(json, classOfT)
    fun <T> fromJson(json: String, classOfT: Class<T>): T = gson.fromJson(json, classOfT)
    fun <T> fromJson(reader: Reader, classOfT: Class<T>): T = gson.fromJson(reader, classOfT)
    fun toJson(src: Any?): String = gson.toJson(src)
    inline fun <reified T> reload(src: Any): T = fromJson(toJson(src))
}