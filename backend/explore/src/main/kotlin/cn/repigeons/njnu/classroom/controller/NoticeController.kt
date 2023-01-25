package cn.repigeons.njnu.classroom.controller

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.njnu.classroom.service.NoticeService
import org.springframework.web.bind.annotation.*

@RestController
//@RequestMapping("notice")
class NoticeController(
    private val noticeService: NoticeService
) {
    @GetMapping("notice")
    fun getNotice(): CommonResponse<*> {
        val data = noticeService.get()
        return CommonResponse.success(data)
    }

    @PostMapping("notice")
    fun setNotice(
        @RequestParam id: Int
    ): CommonResponse<*> {
        val data = noticeService.set(id)
        return CommonResponse.success(data)
    }

    @PutMapping("notice")
    fun addNotice(
        @RequestParam text: String
    ): CommonResponse<*> {
        val data = noticeService.add(text.replace("\\n", "\n"))
        return CommonResponse.success(data)
    }
}