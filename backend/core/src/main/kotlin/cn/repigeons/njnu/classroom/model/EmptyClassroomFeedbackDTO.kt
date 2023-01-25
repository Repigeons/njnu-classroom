package cn.repigeons.njnu.classroom.model

import cn.repigeons.njnu.classroom.enumerate.Weekday

data class EmptyClassroomFeedbackDTO(
    val jc: Short,
    val results: List<EmptyClassroom>,
    val index: Int,
    val weekday: Weekday,
    val jxlmc: String,
)