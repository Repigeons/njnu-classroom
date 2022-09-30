package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.model.EmptyClassroomFeedbackDTO
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.EmptyClassroomService
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("api")
class ActionController(
    private val cacheService: CacheService,
    private val emptyClassroomService: EmptyClassroomService
) {
    @PostMapping("empty/feedback")
    fun feedbackEmptyClassroom(@RequestBody dto: EmptyClassroomFeedbackDTO): JsonResponse {
        emptyClassroomService.feedback(
            dto.jxl,
            Weekday.parse(dto.day)!!,
            dto.jc,
            dto.results,
            dto.index
        )
        return JsonResponse(status = Status.ACCEPTED)
    }

    @PostMapping("flushCache/flushClassroomList")
    fun flushClassroomList(): JsonResponse {
        cacheService.flushClassroomList()
        return JsonResponse(status = Status.ACCEPTED)
    }

    @PostMapping("flushCache/flushBuildingPosition")
    fun flushBuildingPosition(): JsonResponse {
        cacheService.flushBuildingPosition()
        return JsonResponse(status = Status.ACCEPTED)
    }
}