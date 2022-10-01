package cn.repigeons.njnu.classroom.model

data class UserTimetableDTO(
    val id: Long?,
    val openid: String,
    val weekday: String,
    val ksjc: Short,
    val jsjc: Short,
    val place: String,
    val remark: Map<String, *>
)