package cn.repigeons.njnu.classroom.component

import cn.repigeons.commons.api.CommonResponse
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
    fun handle(e: Exception, request: HttpServletRequest): CommonResponse<*> {
        logger.error("全局异常：{} {}", request.method, request.requestURI)
        request.parameterMap.forEach { (key: String, value: Array<String>) ->
            logger.error("*****请求参数*****:{},{}", key, value)
        }
        logger.error("*********异常信息:{}", e.message, e)
        return when {
            e is HttpClientErrorException -> CommonResponse.failed(e.responseMessage)

            e is HttpRequestMethodNotSupportedException -> CommonResponse.failed("请求方法错误[${request.method}]")

            request.method in listOf("POST", "PUT", "DELETE") &&
                    (e is HttpMediaTypeException || e is HttpMessageConversionException) -> {
                val contentType = request.getHeader("Content-Type")
                CommonResponse.failed("请求格式错误[${contentType}]")
            }

            e is MissingServletRequestParameterException ||
                    e is HttpMessageNotReadableException ||
                    e is IllegalArgumentException ->
                CommonResponse.failed(e.responseMessage)

            else -> CommonResponse.failed(e.responseMessage)
        }
    }

    private val Exception.responseMessage: String
        get() = message.takeUnless { it.isNullOrBlank() } ?: "服务器异常"
}