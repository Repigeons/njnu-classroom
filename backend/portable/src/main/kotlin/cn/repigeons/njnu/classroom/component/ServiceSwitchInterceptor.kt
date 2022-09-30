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
    private val switchOffResponse = JsonResponse(
        status = Status.IM_A_TEAPOT,
        message = "service off"
    ).let { GsonUtil.toJson(it) }.toByteArray()

    override fun preHandle(
        request: HttpServletRequest,
        response: HttpServletResponse,
        handler: Any
    ): Boolean {
        if (serviceSwitch.value) return true
        response.contentType = "application/json"
        response.outputStream.use { outputStream ->
            outputStream.write(switchOffResponse)
        }
        return false
    }
}