package cn.repigeons.njnu.classroom.model

data class EmptyClassroomFeedbackDTO(
    val jc: Short,
    val results: List<EmptyClassroom>,
    val index: Int,
    val day: String,
    val jxl: String,
)