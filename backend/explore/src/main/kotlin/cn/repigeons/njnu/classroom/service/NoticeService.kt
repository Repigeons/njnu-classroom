package cn.repigeons.njnu.classroom.service

interface NoticeService {
    fun get(): Map<*, *>
    fun set(id: Int): Map<*, *>
    fun add(text: String): Map<*, *>
}