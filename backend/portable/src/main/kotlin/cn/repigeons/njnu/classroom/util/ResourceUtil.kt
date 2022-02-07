package cn.repigeons.njnu.classroom.util

import java.io.BufferedReader
import java.io.InputStreamReader

object ResourceUtil {
    fun loadResource(name: String): String {
        val stream = javaClass.getResourceAsStream(name)!!
        val reader = BufferedReader(InputStreamReader(stream, "UTF-8"))
        return reader.useLines { lines ->
            lines.joinToString()
        }
    }
}