package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.component.ServiceSwitch
import cn.repigeons.njnu.classroom.model.EmptyClassroomFeedbackDTO
import cn.repigeons.njnu.classroom.service.EmptyClassroomService
import org.slf4j.LoggerFactory
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("api")
class ActionController(
    private val serviceSwitch: ServiceSwitch,
    private val emptyClassroomService: EmptyClassroomService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @PostMapping("switch")
    fun switch(value: Boolean?): JsonResponse {
        serviceSwitch.value = value ?: !serviceSwitch.value
        val message = if (serviceSwitch.value) "service on" else "service off"
        logger.info(message)
        return JsonResponse(
            message = message,
            data = message
        )
    }

    @PostMapping("empty/feedback")
    fun feedbackEmptyClassroom(@RequestBody dto: EmptyClassroomFeedbackDTO): JsonResponse {
        if (!serviceSwitch.value) {
            return JsonResponse(
                status = Status.IM_A_TEAPOT,
                message = "service off"
            )
        }
        emptyClassroomService.feedback(
            dto.jxl,
            Weekday.parse(dto.day)!!,
            dto.jc,
            dto.results,
            dto.index
        )
        return JsonResponse(status = Status.ACCEPTED)
    }
}