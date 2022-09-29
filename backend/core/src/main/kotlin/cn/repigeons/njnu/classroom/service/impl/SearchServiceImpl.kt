package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.PageResult
import cn.repigeons.njnu.classroom.common.PageResult.Companion.pageInfo
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.mbg.model.TimetableRecord
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.SearchService
import com.github.pagehelper.PageHelper
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.elements.isGreaterThanOrEqualTo
import org.mybatis.dynamic.sql.util.kotlin.elements.isLessThanOrEqualTo
import org.mybatis.dynamic.sql.util.kotlin.elements.isLike
import org.springframework.stereotype.Service

@Service
class SearchServiceImpl(
    private val timetableMapper: TimetableMapper
) : SearchService {
    override fun search(
        jcKs: Short,
        jcJs: Short,
        day: Weekday?,
        jxl: String?,
        keyword: String?,
        page: Int,
        size: Int,
    ): JsonResponse {
        PageHelper.startPage<TimetableRecord>(page, size)
        val pageInfo = timetableMapper.select {
            where(TimetableDynamicSqlSupport.Timetable.jcKs, isGreaterThanOrEqualTo(jcKs))
            and(TimetableDynamicSqlSupport.Timetable.jcJs, isLessThanOrEqualTo(jcJs))
            if (day != null)
                and(TimetableDynamicSqlSupport.Timetable.day, isEqualTo(day.value))
            if (jxl != null)
                and(TimetableDynamicSqlSupport.Timetable.jxlmc, isEqualTo(jxl))
            if (keyword != null) {
                val value = "%$keyword%"
                and(TimetableDynamicSqlSupport.Timetable.kcm, isLike(value))
                    .or(TimetableDynamicSqlSupport.Timetable.jyytms, isLike(value))
                if (day != null)
                    and(TimetableDynamicSqlSupport.Timetable.day, isEqualTo(day.value))
                if (jxl != null)
                    and(TimetableDynamicSqlSupport.Timetable.jxlmc, isEqualTo(jxl))
                and(TimetableDynamicSqlSupport.Timetable.jcJs, isLessThanOrEqualTo(jcJs))
                and(TimetableDynamicSqlSupport.Timetable.jcKs, isGreaterThanOrEqualTo(jcKs))
            }
        }.pageInfo()
        val list = pageInfo.list.map {
            QueryResultItem(it)
        }
        val result = PageResult(list, pageInfo)
        return JsonResponse(data = result)
    }
}