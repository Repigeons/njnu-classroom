package cn.repigeons.njnu.classroom.util

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.Reader

object GsonUtil {
    val gson: Gson = GsonBuilder().serializeNulls().enableComplexMapKeySerialization().disableHtmlEscaping().create()
    inline fun <reified T> fromJson(json: String): T = gson.fromJson(json, object : TypeToken<T>() {}.type)
    inline fun <reified T> fromJson(json: Reader): T = gson.fromJson(json, object : TypeToken<T>() {}.type)
    fun toJson(src: Any?): String = gson.toJson(src)
}