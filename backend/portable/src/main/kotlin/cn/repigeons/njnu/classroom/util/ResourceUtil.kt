package cn.repigeons.njnu.classroom.util

import java.io.BufferedReader
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets

object ResourceUtil {
    fun loadResourceText(name: String): String? =
        javaClass.getResourceAsStream(name)?.use { stream ->
            BufferedReader(InputStreamReader(stream, StandardCharsets.UTF_8))
                .useLines { lines ->
                    lines.joinToString("")
                }
        }
}