package cn.repigeons.njnu.classroom.controller

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.commons.utils.GsonUtils
import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.UserTimetableRecord
import cn.repigeons.njnu.classroom.model.UserTimetableDTO
import cn.repigeons.njnu.classroom.model.UserTimetableVO
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
    ): CommonResponse<*> {
        val openid = token2openid(token)
            ?: return CommonResponse.unauthorized()
        val records = userTimetableMapper.select {
            where(UserTimetableDynamicSqlSupport.UserTimetable.openid, isEqualTo(openid))
        }
        val data = records.map { record ->
            UserTimetableVO(
                weekday = record.weekday!!,
                ksjc = record.ksjc!!,
                jsjc = record.jsjc!!,
                place = record.place!!,
                remark = GsonUtils.fromJson(record.remark!!)
            )
        }
        return CommonResponse.success(data)
    }

    /**
     * 新增/修改用户时间表
     */
    @PostMapping("timetable/save")
    fun saveTimetable(
        @RequestHeader("Authorization") token: String,
        @RequestBody payload: UserTimetableDTO
    ): CommonResponse<*> {
        val openid = token2openid(token)
            ?: return CommonResponse.unauthorized()
        val record = UserTimetableRecord(
            id = payload.id,
            openid = openid,
            weekday = payload.weekday,
            ksjc = payload.ksjc,
            jsjc = payload.jsjc,
            place = payload.place,
            remark = GsonUtils.toJson(payload.remark)
        )
        if (record.id == null)
            userTimetableMapper.insert(record)
        else
            userTimetableMapper.updateByPrimaryKey(record)
        return CommonResponse.success(
            mapOf(
                "id" to record.id
            )
        )
    }

    @PostMapping("timetable/delete")
    fun deleteTimetable(
        @RequestHeader("Authorization") token: String,
        @RequestBody payload: Map<String, Long>
    ): CommonResponse<*> {
        val openid = token2openid(token)
            ?: return CommonResponse.unauthorized()
        val id = requireNotNull(payload["id"]) { "请求参数缺失：id" }
        val record = userTimetableMapper.selectByPrimaryKey(id)
            ?: return CommonResponse.failed("记录不存在")
        if (record.openid != openid)
            return CommonResponse.forbidden()
        return CommonResponse.success()
    }

    private fun token2openid(token: String): String? {
        if (!token.startsWith(JwtUtil.TOKEN_HEAD)) return null
        val claims = JwtUtil.parse(token.substring(JwtUtil.TOKEN_HEAD.length))
            ?: return null
        return claims.subject
    }
}