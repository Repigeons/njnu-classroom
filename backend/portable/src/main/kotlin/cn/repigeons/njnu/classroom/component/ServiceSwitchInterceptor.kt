package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.controller.ServiceSwitch
import cn.repigeons.njnu.classroom.util.GsonUtil
import org.springframework.stereotype.Component
import org.springframework.web.servlet.HandlerInterceptor
import javax.servlet.http.HttpServletRequest
import javax.servlet.http.HttpServletResponse

@Component
class ServiceSwitchInterceptor(
    private val serviceSwitch: ServiceSwitch
) : HandlerInterceptor {
    override fun preHandle(
        request: HttpServletRequest,
        response: HttpServletResponse,
        handler: Any
    ): Boolean {
        if (serviceSwitch.value) return true
        val result = JsonResponse(
            status = Status.IM_A_TEAPOT,
            message = "service off"
        )
        response.contentType = "application/json"
        response.outputStream.use { outputStream ->
            outputStream.write(
                GsonUtil.toJson(result).toByteArray()
            )
        }
        return false
    }
}