package cn.repigeons.njnu.classroom.util

import java.io.BufferedReader
import java.io.InputStreamReader

object ResourceUtil {
    fun loadResourceText(name: String): String? =
        javaClass.getResourceAsStream(name)?.use {
            BufferedReader(InputStreamReader(it, "UTF-8"))
        }?.useLines { lines ->
            lines.joinToString("")
        }
}