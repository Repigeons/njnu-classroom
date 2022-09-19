package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.service.GridsService
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("explore")
class GridsController(
    private val gridsService: GridsService
) {
    @GetMapping("grids.json")
    fun getGrids(): JsonResponse {
        return JsonResponse(
            data = gridsService.getGrids()
        )
    }

    @PostMapping("grids/reload")
    fun flushShuttleLine(): JsonResponse {
        gridsService.flushGrids()
        return JsonResponse(status = Status.ACCEPTED)
    }

    init {
        gridsService.flushGrids()
    }
}