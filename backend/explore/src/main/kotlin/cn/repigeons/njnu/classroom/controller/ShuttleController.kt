package cn.repigeons.njnu.classroom.controller

import cn.repigeons.commons.api.CommonResponse
import cn.repigeons.commons.redisTemplate.RedisService
import cn.repigeons.njnu.classroom.enumerate.Weekday
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
        @RequestParam(required = false) weekday: Weekday?
    ): CommonResponse<*> {
        if (weekday == null)
            return CommonResponse.success(
                mapOf(
                    "stations" to shuttleService.getStationPosition()
                )
            )
        val direction1 = redisService["explore:shuttle:${weekday.name}:1"] as List<*>
        val direction2 = redisService["explore:shuttle:${weekday.name}:2"] as List<*>
        return CommonResponse.success(
            mapOf(
                "stations" to shuttleService.getStationPosition(),
                "direction1" to direction1,
                "direction2" to direction2,
            )
        )
    }

    @PostMapping("shuttle/upload")
    fun uploadShuttleImage(
        @RequestParam file: MultipartFile
    ): CommonResponse<*> {
        shuttleService.sendShuttleImage(file.originalFilename, file.bytes)
        return CommonResponse.success()
    }

    @PutMapping("shuttle/upload")
    fun uploadShuttleImage(
        @RequestParam(required = false) filename: String?,
        @RequestBody bytes: ByteArray
    ): CommonResponse<*> {
        shuttleService.sendShuttleImage(filename, bytes)
        return CommonResponse.success()
    }

    @Scheduled(cron = "0 0 7 * * *")
    @PostMapping("shuttle/reload")
    fun flushShuttleLine(): CommonResponse<*> {
        shuttleService.flushStationPosition()
        shuttleService.flushRoute()
        return CommonResponse.success()
    }

    init {
        shuttleService.flushStationPosition()
        shuttleService.flushRoute()
    }
}