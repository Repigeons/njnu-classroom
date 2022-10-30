package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.UserTimetableRecord
import cn.repigeons.njnu.classroom.model.UserTimetableDTO
import cn.repigeons.njnu.classroom.model.UserTimetableVO
import cn.repigeons.njnu.classroom.util.GsonUtil
import cn.repigeons.njnu.classroom.util.JwtUtil
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.springframework.web.bind.annotation.*

/**
 * 用户时间表
 */
@RestController
@RequestMapping("explore/user")
class UserTimetableController(
    private val userTimetableMapper: UserTimetableMapper
) {
    /**
     * 查询用户时间表
     */
    @GetMapping("timetable.json")
    fun getTimeTable(
        @RequestHeader("Authorization") token: String
    ): JsonResponse {
        val openid = token2openid(token)
            ?: return JsonResponse(status = Status.UNAUTHORIZED)
        val records = userTimetableMapper.select {
            where(UserTimetableDynamicSqlSupport.UserTimetable.openid, isEqualTo(openid))
        }
        val data = records.map { record ->
            UserTimetableVO(
                weekday = record.weekday!!,
                ksjc = record.ksjc!!,
                jsjc = record.jsjc!!,
                place = record.place!!,
                remark = GsonUtil.fromJson(record.remark!!)
            )
        }
        return JsonResponse(
            data = data
        )
    }

    /**
     * 新增/修改用户时间表
     */
    @PostMapping("timetable/save")
    fun saveTimetable(
        @RequestHeader("Authorization") token: String,
        @RequestBody payload: UserTimetableDTO
    ): JsonResponse {
        val openid = token2openid(token)
            ?: return JsonResponse(status = Status.UNAUTHORIZED)
        val record = UserTimetableRecord(
            id = payload.id,
            openid = openid,
            weekday = payload.weekday,
            ksjc = payload.ksjc,
            jsjc = payload.jsjc,
            place = payload.place,
            remark = GsonUtil.toJson(payload.remark)
        )
        if (record.id == null)
            userTimetableMapper.insert(record)
        else
            userTimetableMapper.updateByPrimaryKey(record)
        return JsonResponse(
            Pair("id", record.id)
        )
    }

    @PostMapping("timetable/delete")
    fun deleteTimetable(
        @RequestHeader("Authorization") token: String,
        @RequestBody payload: Map<String, Long>
    ): JsonResponse {
        val openid = token2openid(token)
            ?: return JsonResponse(status = Status.UNAUTHORIZED)
        val id = requireNotNull(payload["id"]) { "请求参数缺失：id" }
        val record = userTimetableMapper.selectByPrimaryKey(id)
            ?: return JsonResponse(
                status = Status.NOT_FOUND,
                message = "记录不存在"
            )
        if (record.openid != openid)
            return JsonResponse(
                status = Status.FORBIDDEN
            )
        return JsonResponse()
    }

    private fun token2openid(token: String): String? {
        if (!token.startsWith(JwtUtil.TOKEN_HEAD)) return null
        val claims = JwtUtil.parse(token.substring(JwtUtil.TOKEN_HEAD.length))
            ?: return null
        return claims.subject
    }
}