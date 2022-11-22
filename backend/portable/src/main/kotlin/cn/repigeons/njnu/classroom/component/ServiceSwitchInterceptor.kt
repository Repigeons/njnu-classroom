package cn.repigeons.njnu.classroom.component

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.commons.utils.GsonUtils
import cn.repigeons.njnu.classroom.controller.ServiceSwitch
import org.springframework.http.HttpStatus
import org.springframework.stereotype.Component
import org.springframework.web.servlet.HandlerInterceptor
import javax.servlet.http.HttpServletRequest
import javax.servlet.http.HttpServletResponse

@Component
class ServiceSwitchInterceptor(
    private val serviceSwitch: ServiceSwitch
) : HandlerInterceptor {
    private val switchOffResponse = CommonResponse.success(
        message = "service off",
        data = null,
    ).let { response ->
        with(response.javaClass.getDeclaredField("status")) {
            isAccessible = true
            set(response, HttpStatus.I_AM_A_TEAPOT.value())
        }
        GsonUtils.toJson(response)
    }.toByteArray()

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