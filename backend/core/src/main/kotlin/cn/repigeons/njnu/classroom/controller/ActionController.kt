package cn.repigeons.njnu.classroom.controller

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.njnu.classroom.model.EmptyClassroomFeedbackDTO
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.EmptyClassroomService
import org.springframework.scheduling.annotation.Scheduled
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
    fun feedbackEmptyClassroom(@RequestBody dto: EmptyClassroomFeedbackDTO): CommonResponse<*> {
        emptyClassroomService.feedback(
            jxlmc = dto.jxlmc,
            weekday = dto.weekday,
            jc = dto.jc,
            results = dto.results,
            index = dto.index,
        )
        return CommonResponse.success()
    }

    @Scheduled(cron = "0 0 7 * * *")
    @PostMapping("classrooms/reload")
    fun flushClassroomList(): CommonResponse<*> {
        cacheService.flushClassroomList()
        return CommonResponse.success()
    }

    @Scheduled(cron = "0 0 7 * * *")
    @PostMapping("position/reload")
    fun flushBuildingPosition(): CommonResponse<*> {
        cacheService.flushBuildingPosition()
        return CommonResponse.success()
    }
}