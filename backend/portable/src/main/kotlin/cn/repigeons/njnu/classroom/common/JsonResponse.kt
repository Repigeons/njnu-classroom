package cn.repigeons.njnu.classroom.common

class JsonResponse(
    status: Status = Status.SUCCESS,
    var message: String? = null,
    val data: Any? = null,
) {
    val status: Int

    init {
        this.status = status.code
        message = message ?: status.message
    }
}

enum class Status(val code: Int, val message: String?) {
    SUCCESS(200, null),
    ACCEPTED(202, null),
    BAD_REQUEST(400, "错误请求"),
    UNAUTHORIZED(401, "未授权访问"),
    FORBIDDEN(403, "禁止访问"),
    NOT_FOUND(404, "找不到资源"),
    METHOD_NOT_ALLOWED(405, "请求方法错误"),
    FAILED(500, "服务器异常"),
    IM_A_TEAPOT(418, null)
}