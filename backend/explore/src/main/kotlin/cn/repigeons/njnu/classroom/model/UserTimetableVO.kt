package cn.repigeons.njnu.classroom.model

data class UserTimetableVO(
    val weekday: String,
    val ksjc: Short,
    val jsjc: Short,
    val place: String,
    val remark: Map<String, *>
)