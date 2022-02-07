package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.component.StaticData
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("explore")
class GridsController(
    private val staticData: StaticData
) {
    @GetMapping("grids.json")
    fun getGrids(): JsonResponse {
        return JsonResponse(
            data = staticData.grids
        )
    }
}