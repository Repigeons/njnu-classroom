package cn.repigeons.njnu.classroom.configuration

import org.slf4j.LoggerFactory
import org.springframework.http.HttpRequest
import org.springframework.http.client.ClientHttpRequestExecution
import org.springframework.http.client.ClientHttpRequestInterceptor
import org.springframework.http.client.ClientHttpResponse
import java.io.BufferedReader
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets

internal class RestTemplateRequestInterceptor : ClientHttpRequestInterceptor {
    private val logger = LoggerFactory.getLogger(javaClass)

    override fun intercept(
        request: HttpRequest,
        body: ByteArray,
        execution: ClientHttpRequestExecution
    ): ClientHttpResponse {
        traceRequest(request, body)
        val response = execution.execute(request, body)
        traceResponse(response)
        return response
    }

    private fun traceRequest(request: HttpRequest, body: ByteArray) {
        logger.debug("===========================request begin================================================")
        logger.debug("URI         : {}", request.uri)
        logger.debug("Method      : {}", request.method)
        logger.debug("Headers     : {}", request.headers)
        logger.debug("Request body: {}", String(body, StandardCharsets.UTF_8))
        logger.debug("==========================request end================================================")
    }

    private fun traceResponse(response: ClientHttpResponse) {
        logger.debug("============================response begin==========================================")
        logger.debug("Status code  : {}", response.statusCode)
        logger.debug("Status text  : {}", response.statusText)
        logger.debug("Headers      : {}", response.headers)
        val inputStringBuilder = StringBuilder()
        BufferedReader(InputStreamReader(response.body, StandardCharsets.UTF_8)).use { bufferedReader ->
            var line = bufferedReader.readLine()
            while (line != null) {
                inputStringBuilder.append(line)
                inputStringBuilder.append('\n')
                line = bufferedReader.readLine()
            }
        }
        logger.debug("Response body: {}", inputStringBuilder)
        logger.debug("=======================response end=================================================")
    }
}