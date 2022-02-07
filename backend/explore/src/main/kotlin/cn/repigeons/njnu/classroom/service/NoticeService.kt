package cn.repigeons.njnu.classroom.service

import com.alibaba.fastjson.JSONObject

interface NoticeService {
    fun getNotice(): JSONObject
    fun setNotice(id: Int): JSONObject
    fun addNotice(text: String): JSONObject
}