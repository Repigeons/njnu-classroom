package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.model.EmptyClassroom

interface EmptyClassroomService {
    fun getEmptyClassrooms(jxl: String, day: Weekday?, jc: Short): JsonResponse
    fun feedback(
        jxl: String,
        day: Weekday,
        jc: Short,
        results: List<EmptyClassroom>,
        index: Int,
    )
}