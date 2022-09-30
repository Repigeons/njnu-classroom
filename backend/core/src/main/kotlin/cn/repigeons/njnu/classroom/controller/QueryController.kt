package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.component.Resources
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
        @RequestParam day: String,
        @RequestParam jc: Short,
    ): JsonResponse {
        return emptyClassroomService.getEmptyClassrooms(jxl, Weekday.parse(day), jc)
    }

    @GetMapping("overview.json")
    fun getOverview(
        @RequestParam jasdm: String
    ): JsonResponse {
        return overviewService.getOverview(jasdm)
    }

    @GetMapping("search.json")
    fun getSearch(
        @RequestParam day: String,
        @RequestParam jcKs: Short,
        @RequestParam jcJs: Short,
        @RequestParam jxl: String,
        @RequestParam("kcm") keyword: String,
        @RequestParam(defaultValue = "1") page: Int,
        @RequestParam(defaultValue = "10") size: Int
    ): JsonResponse {
        return searchService.search(
            jcKs = jcKs,
            jcJs = jcJs,
            day = Weekday.parse(day),
            jxl = if (jxl == "#" || jxl.isEmpty()) null else jxl,
            keyword = if (keyword == "#" || keyword.isBlank()) null else keyword,
            page = page,
            size = size
        )
    }

    @GetMapping("classrooms.json")
    fun getClassroomList() = JsonResponse(data = cacheService.getClassroomList())

    @GetMapping("position.json")
    fun getPosition() = JsonResponse(data = cacheService.getBuildingPosition())

    @GetMapping("zylxdm.json")
    fun getZylxdm() = JsonResponse(data = resources.zylxdm)
}