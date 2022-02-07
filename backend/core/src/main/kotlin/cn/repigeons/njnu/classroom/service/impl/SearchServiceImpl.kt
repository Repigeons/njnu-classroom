package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.PageResult
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.ProRecord
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.SearchService
import com.github.pagehelper.PageHelper
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.elements.isGreaterThanOrEqualTo
import org.mybatis.dynamic.sql.util.kotlin.elements.isLessThanOrEqualTo
import org.mybatis.dynamic.sql.util.kotlin.elements.isLike
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

@Service
class SearchServiceImpl(
    private val devMapper: DevMapper,
    private val proMapper: ProMapper,
    @Value("env") private val env: String
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
        val result: PageResult<*> = if (env == "pro") {
            PageHelper.startPage<ProRecord>(page, size)
            val records = proMapper.select {
                where(ProDynamicSqlSupport.Pro.jcKs, isGreaterThanOrEqualTo(jcKs))
                and(ProDynamicSqlSupport.Pro.jcJs, isLessThanOrEqualTo(jcJs))
                if (day != null)
                    and(ProDynamicSqlSupport.Pro.day, isEqualTo(day.value))
                if (jxl != null)
                    and(ProDynamicSqlSupport.Pro.jxlmc, isEqualTo(jxl))
                if (keyword != null) {
                    val value = "%$keyword%"
                    and(ProDynamicSqlSupport.Pro.kcm, isLike(value))
                        .or(ProDynamicSqlSupport.Pro.jyytms, isLike(value))
                    if (day != null)
                        and(ProDynamicSqlSupport.Pro.day, isEqualTo(day.value))
                    if (jxl != null)
                        and(ProDynamicSqlSupport.Pro.jxlmc, isEqualTo(jxl))
                    and(ProDynamicSqlSupport.Pro.jcJs, isLessThanOrEqualTo(jcJs))
                    and(ProDynamicSqlSupport.Pro.jcKs, isGreaterThanOrEqualTo(jcKs))
                }
            }
            val result = PageResult(records)
            val list = result.list.map {
                QueryResultItem(it)
            }
            result.javaClass
                .getDeclaredField("list")
                .apply {
                    isAccessible = true
                    set(result, list)
                }
            result
        } else {
            PageHelper.startPage<ProRecord>(page, size)
            val records = devMapper.select {
                where(DevDynamicSqlSupport.Dev.jcKs, isGreaterThanOrEqualTo(jcKs))
                and(DevDynamicSqlSupport.Dev.jcJs, isLessThanOrEqualTo(jcJs))
                if (day != null)
                    and(DevDynamicSqlSupport.Dev.day, isEqualTo(day.value))
                if (jxl != null)
                    and(DevDynamicSqlSupport.Dev.jxlmc, isEqualTo(jxl))
                if (keyword != null) {
                    val value = "%$keyword%"
                    and(DevDynamicSqlSupport.Dev.kcm, isLike(value))
                        .or(DevDynamicSqlSupport.Dev.jyytms, isLike(value))
                    if (day != null)
                        and(DevDynamicSqlSupport.Dev.day, isEqualTo(day.value))
                    if (jxl != null)
                        and(DevDynamicSqlSupport.Dev.jxlmc, isEqualTo(jxl))
                    and(DevDynamicSqlSupport.Dev.jcJs, isLessThanOrEqualTo(jcJs))
                    and(DevDynamicSqlSupport.Dev.jcKs, isGreaterThanOrEqualTo(jcKs))
                }
            }
            val result = PageResult(records)
            val list = result.list.map {
                QueryResultItem(it)
            }
            result.javaClass
                .getDeclaredField("list")
                .apply {
                    isAccessible = true
                    set(result, list)
                }
            result
        }
        return JsonResponse(data = result)
    }
}