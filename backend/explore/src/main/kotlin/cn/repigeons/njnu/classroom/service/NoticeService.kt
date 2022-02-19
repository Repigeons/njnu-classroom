package cn.repigeons.njnu.classroom.service

import com.alibaba.fastjson.JSONObject

interface NoticeService {
    fun get(): JSONObject
    fun set(id: Int): JSONObject
    fun add(text: String): JSONObject
}