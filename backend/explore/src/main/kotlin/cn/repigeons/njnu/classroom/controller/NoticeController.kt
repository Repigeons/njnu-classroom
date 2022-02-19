package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.service.NoticeService
import org.springframework.web.bind.annotation.*
import kotlin.concurrent.thread

@RestController
@RequestMapping("notice")
class NoticeController(
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
        val data = noticeService.add(text)
        return JsonResponse(data = data)
    }

    init {
        thread { noticeService.get() }
    }
}