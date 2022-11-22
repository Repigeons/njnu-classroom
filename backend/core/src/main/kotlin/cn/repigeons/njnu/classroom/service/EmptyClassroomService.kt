package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.enumerate.Weekday
import cn.repigeons.njnu.classroom.model.EmptyClassroom
import java.util.concurrent.Future

interface EmptyClassroomService {
    fun getEmptyClassrooms(jxl: String, weekday: Weekday?, jc: Short): List<EmptyClassroom>
    fun feedback(
        jxl: String,
        weekday: Weekday,
        jc: Short,
        results: List<EmptyClassroom>,
        index: Int,
    ): Future<*>
}