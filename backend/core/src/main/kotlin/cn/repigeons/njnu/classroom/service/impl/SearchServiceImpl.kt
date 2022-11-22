package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.commons.api.CommonPageable
import cn.repigeons.njnu.classroom.enumerate.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.mbg.model.TimetableRecord
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.SearchService
import com.github.pagehelper.PageHelper
import com.github.pagehelper.PageInfo
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
        weekday: Weekday?,
        jxl: String?,
        keyword: String?,
        page: Int,
        size: Int,
    ): CommonPageable<QueryResultItem> {
        PageHelper.startPage<TimetableRecord>(page, size)
        val records = timetableMapper.select {
            where(TimetableDynamicSqlSupport.Timetable.jcKs, isGreaterThanOrEqualTo(jcKs))
            and(TimetableDynamicSqlSupport.Timetable.jcJs, isLessThanOrEqualTo(jcJs))
            weekday?.run {
                and(TimetableDynamicSqlSupport.Timetable.weekday, isEqualTo(this.name))
            }
            jxl?.run {
                and(TimetableDynamicSqlSupport.Timetable.jxlmc, isEqualTo(this))
            }
            keyword?.run {
                val value = "%$this%"
                and(TimetableDynamicSqlSupport.Timetable.kcm, isLike(value))
                    .or(TimetableDynamicSqlSupport.Timetable.jyytms, isLike(value))
                weekday?.run {
                    and(TimetableDynamicSqlSupport.Timetable.weekday, isEqualTo(this.name))
                }
                jxl?.run {
                    and(TimetableDynamicSqlSupport.Timetable.jxlmc, isEqualTo(this))
                }
                and(TimetableDynamicSqlSupport.Timetable.jcJs, isLessThanOrEqualTo(jcJs))
                and(TimetableDynamicSqlSupport.Timetable.jcKs, isGreaterThanOrEqualTo(jcKs))
            }
        }
        val pageInfo = PageInfo(records)
        val list = pageInfo.list.map {
            QueryResultItem(it)
        }
        return CommonPageable(list, pageInfo)
    }
}