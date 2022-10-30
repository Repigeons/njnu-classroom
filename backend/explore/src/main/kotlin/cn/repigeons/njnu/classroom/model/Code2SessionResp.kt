package cn.repigeons.njnu.classroom.model

data class Code2SessionResp(
    val errcode: Int,
    val errmsg: String,
    val openid: String?,
    val session_key: String?,
    val unionid: String?,
)
