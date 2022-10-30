package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.service.ShuttleService
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile

@RestController
@RequestMapping("explore")
class ShuttleController(
    private val redisService: RedisService,
    private val shuttleService: ShuttleService
) {
    @GetMapping("shuttle.json")
    fun getShuttle(
        @RequestParam day: String?
    ): JsonResponse {
        if (day.isNullOrBlank())
            return JsonResponse(
                data = mapOf(
                    Pair("stations", shuttleService.getStationPosition()),
                )
            )
        val weekday = requireNotNull(Weekday.parse(day)) { Status.BAD_REQUEST.message }
        val direction1: List<*> = redisService["explore:shuttle:${weekday.value}:1"]!!
        val direction2: List<*> = redisService["explore:shuttle:${weekday.value}:2"]!!
        return JsonResponse(
            data = mapOf(
                Pair("stations", shuttleService.getStationPosition()),
                Pair("direction1", direction1),
                Pair("direction2", direction2)
            )
        )
    }

    @PostMapping("shuttle/upload")
    fun uploadShuttleImage(
        @RequestParam file: MultipartFile
    ): JsonResponse {
        shuttleService.sendShuttleImage(file.originalFilename, file.bytes)
        return JsonResponse(status = Status.ACCEPTED)
    }

    @PutMapping("shuttle/upload")
    fun uploadShuttleImage(
        @RequestParam(required = false) filename: String?,
        @RequestBody bytes: ByteArray
    ): JsonResponse {
        shuttleService.sendShuttleImage(filename, bytes)
        return JsonResponse(status = Status.ACCEPTED)
    }

    @Scheduled(cron = "0 0 7 * * *")
    @PostMapping("shuttle/reload")
    fun flushShuttleLine(): JsonResponse {
        shuttleService.flushStationPosition()
        shuttleService.flushRoute()
        return JsonResponse(status = Status.ACCEPTED)
    }

    init {
        shuttleService.flushStationPosition()
        shuttleService.flushRoute()
    }
}