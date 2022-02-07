package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.service.NoticeService
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("notice")
class NoticeController(
    private val noticeService: NoticeService
) {
    @GetMapping("get")
    fun getNotice(): JsonResponse {
        val data = noticeService.getNotice()
        return JsonResponse(data = data)
    }

    @PostMapping("set")
    fun setNotice(
        @RequestParam id: Int
    ): JsonResponse {
        val data = noticeService.setNotice(id)
        return JsonResponse(data = data)
    }

    @PutMapping("add")
    fun addNotice(
        @RequestParam text: String
    ): JsonResponse {
        val data = noticeService.addNotice(text)
        return JsonResponse(data = data)
    }
}