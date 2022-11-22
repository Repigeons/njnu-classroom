package cn.repigeons.njnu.classroom.controller

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.njnu.classroom.component.Resources
import cn.repigeons.njnu.classroom.enumerate.Weekday
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.EmptyClassroomService
import cn.repigeons.njnu.classroom.service.OverviewService
import cn.repigeons.njnu.classroom.service.SearchService
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("api")
class QueryController(
    private val resources: Resources,
    private val cacheService: CacheService,
    private val emptyClassroomService: EmptyClassroomService,
    private val overviewService: OverviewService,
    private val searchService: SearchService
) {
    @GetMapping("empty.json")
    fun getEmpty(
        @RequestParam jxl: String,
        @RequestParam weekday: Weekday,
        @RequestParam jc: Short,
    ): CommonResponse<*> {
        val result = emptyClassroomService.getEmptyClassrooms(jxl, weekday, jc)
        return CommonResponse.success(result)
    }

    @GetMapping("overview.json")
    fun getOverview(
        @RequestParam jasdm: String
    ): CommonResponse<*> {
        val result = overviewService.getOverview(jasdm)
        return CommonResponse.success(result)
    }

    @GetMapping("search.json")
    fun getSearch(
        @RequestParam weekday: Weekday,
        @RequestParam jcKs: Short,
        @RequestParam jcJs: Short,
        @RequestParam jxl: String,
        @RequestParam("kcm") keyword: String,
        @RequestParam(defaultValue = "1") page: Int,
        @RequestParam(defaultValue = "10") size: Int
    ): CommonResponse<*> {
        val result = searchService.search(
            jcKs = jcKs,
            jcJs = jcJs,
            weekday = weekday,
            jxl = if (jxl == "#" || jxl.isEmpty()) null else jxl,
            keyword = if (keyword == "#" || keyword.isBlank()) null else keyword,
            page = page,
            size = size
        )
        return CommonResponse.success(result)
    }

    @GetMapping("classrooms.json")
    fun getClassroomList() = CommonResponse.success(cacheService.getClassroomList())

    @GetMapping("position.json")
    fun getPosition() = CommonResponse.success(cacheService.getBuildingPosition())

    @GetMapping("zylxdm.json")
    fun getZylxdm() = CommonResponse.success(resources.zylxdm)
}