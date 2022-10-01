package cn.repigeons.njnu.classroom.common

/**
 * 标准响应格式
 */
class JsonResponse {
    val status: Int
    val message: String
    val data: Any?

    constructor(
        status: Status = Status.SUCCESS,
        message: String? = null,
        data: Any? = null
    ) {
        this.status = status.code
        this.message = message ?: status.message
        this.data = data
    }

    constructor(vararg data: Pair<String, *>) : this(data = mapOf(*data))
}

/**
 * 通用响应状态
 */
enum class Status(val code: Int, val message: String) {
    SUCCESS(200, "OK"),
    ACCEPTED(202, "ACCEPTED"),
    BAD_REQUEST(400, "错误请求"),
    UNAUTHORIZED(401, "未授权访问"),
    FORBIDDEN(403, "禁止访问"),
    NOT_FOUND(404, "找不到资源"),
    METHOD_NOT_ALLOWED(405, "请求方法错误"),
    FAILED(500, "服务器异常"),
    IM_A_TEAPOT(418, "我是一个茶壶")
}