package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import org.slf4j.LoggerFactory
import org.springframework.http.converter.HttpMessageConversionException
import org.springframework.http.converter.HttpMessageNotReadableException
import org.springframework.web.HttpMediaTypeException
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
class GlobalExceptionHandler {
    private val logger = LoggerFactory.getLogger(javaClass)

    @ResponseBody
    @ExceptionHandler(Exception::class)
    fun handle(e: Exception, request: HttpServletRequest): JsonResponse {
        logger.error("全局异常：{} {}", request.method, request.requestURI)
        request.parameterMap.forEach { (key: String, value: Array<String>) ->
            logger.error("*****请求参数*****:{},{}", key, value)
        }
        logger.error("*********异常信息:{}", e.message, e)
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
                    message = "请求方法错误[${request.method}]"
                )
            }

            request.method in listOf("POST", "PUT", "DELETE") &&
                    (e is HttpMediaTypeException || e is HttpMessageConversionException) -> {
                val contentType = request.getHeader("Content-Type")
                JsonResponse(
                    status = Status.BAD_REQUEST,
                    message = "请求格式错误[${contentType}]"
                )
            }

            e is MissingServletRequestParameterException || e is HttpMessageNotReadableException -> {
                JsonResponse(
                    status = Status.BAD_REQUEST,
                    message = e.message
                )
            }

            else -> {
                JsonResponse(
                    status = Status.FAILED,
                    message = e.message.takeUnless { it.isNullOrBlank() } ?: "服务器异常"
                )
            }
        }
    }
}