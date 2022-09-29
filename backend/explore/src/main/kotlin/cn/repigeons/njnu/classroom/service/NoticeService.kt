package cn.repigeons.njnu.classroom.service

interface NoticeService {
    fun get(): Map<String, *>
    fun set(id: Int): Map<*, *>
    fun add(text: String): Map<*, *>
}