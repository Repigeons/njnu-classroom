package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.service.MailService
import org.slf4j.LoggerFactory
import org.springframework.web.HttpMediaTypeNotSupportedException
import org.springframework.web.HttpRequestMethodNotSupportedException
import org.springframework.web.bind.MissingServletRequestParameterException
import org.springframework.web.bind.annotation.ControllerAdvice
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.ResponseBody
import org.springframework.web.client.HttpClientErrorException
import javax.servlet.http.HttpServletRequest

/**
 * 全局异常处理
 */
@ControllerAdvice
class GlobalExceptionHandler(
    private val mailService: MailService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    @ResponseBody
    @ExceptionHandler(Exception::class)
    fun handle(e: Exception, request: HttpServletRequest): JsonResponse {
        logger.error("### {} {}", request.method, request.requestURI)
        request.parameterMap.forEach { (key: String, value: Array<String>) ->
            logger.error("### {}={}", key, value)
        }
        logger.error("### {} {}", e.message, e)
        return when {
            e is HttpClientErrorException -> {
                JsonResponse(
                    status = Status.FAILED,
                    message = e.message
                )
            }
            e is HttpRequestMethodNotSupportedException -> {
                JsonResponse(
                    status = Status.METHOD_NOT_ALLOWED,
                    message = "Method Not Allowed: ${request.method}"
                )
            }
            e is HttpMediaTypeNotSupportedException && request.method in listOf("POST", "PUT", "DELETE") -> {
                val contentType = request.getHeader("Content-Type")
                JsonResponse(
                    status = Status.BAD_REQUEST,
                    message = "Content-Type: $contentType"
                )
            }
            e is MissingServletRequestParameterException -> {
                JsonResponse(
                    status = Status.BAD_REQUEST,
                    message = "参数缺失: ${e.parameterName}"
                )
            }
            else -> {
                val stackTrace = e.stackTrace?.joinToString("") {
                    "\n" + "${it.className}\n" +
                            "${it.fileName}  " +
                            "${it.lineNumber}\n" +
                            "${it.methodName}\n"
                }
                mailService.sendPlain(
                    subject = "【南师教室】错误报告",
                    content = e.message + e.toString() + stackTrace
                )
                JsonResponse(
                    status = Status.FAILED,
                    message = "服务器异常"
                )
            }
        }
    }
}