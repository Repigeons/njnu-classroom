package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.component.ServiceSwitch
import cn.repigeons.njnu.classroom.component.StaticData
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.service.ShuttleService
import com.alibaba.fastjson.JSON
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile


@RestController
@RequestMapping("explore")
class ShuttleController(
    private val serviceSwitch: ServiceSwitch,
    private val staticData: StaticData,
    private val redisService: RedisService,
    private val shuttleService: ShuttleService
) {
    @GetMapping("shuttle.json")
    fun getShuttle(
        @RequestParam day: String?
    ): JsonResponse {
        if (!serviceSwitch.value) {
            return JsonResponse(
                status = Status.IM_A_TEAPOT,
                message = "service off"
            )
        }
        if (day.isNullOrBlank())
            return JsonResponse(
                data = mapOf(
                    Pair("stations", staticData.shuttleStationPosition),
                )
            )
        val weekday = Weekday.parse(day)
            ?: return JsonResponse(status = Status.BAD_REQUEST)
        val direction1 = JSON.parseArray(redisService["explore:shuttle:${weekday.value}:1"])
        val direction2 = JSON.parseArray(redisService["explore:shuttle:${weekday.value}:2"])
        return JsonResponse(
            data = mapOf(
                Pair("stations", staticData.shuttleStationPosition),
                Pair("direction1", direction1),
                Pair("direction2", direction2)
            )
        )
    }

    @PostMapping("shuttle/upload")
    fun uploadShuttleImage(
        @RequestParam file: MultipartFile
    ): JsonResponse {
        shuttleService.sendShuttleImage(file)
        return JsonResponse(status = Status.ACCEPTED)
    }
}