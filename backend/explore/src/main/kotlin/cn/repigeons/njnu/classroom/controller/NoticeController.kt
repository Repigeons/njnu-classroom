package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.service.NoticeService
import org.springframework.core.task.TaskExecutor
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("notice")
class NoticeController(
    taskExecutor: TaskExecutor,
    private val noticeService: NoticeService
) {
    @GetMapping("get")
    fun getNotice(): JsonResponse {
        val data = noticeService.get()
        return JsonResponse(data = data)
    }

    @PostMapping("set")
    fun setNotice(
        @RequestParam id: Int
    ): JsonResponse {
        val data = noticeService.set(id)
        return JsonResponse(data = data)
    }

    @PutMapping("add")
    fun addNotice(
        @RequestParam text: String
    ): JsonResponse {
        val data = noticeService.add(text.replace("\\n", "\n"))
        return JsonResponse(data = data)
    }

    init {
        taskExecutor.execute { noticeService.get() }
    }
}