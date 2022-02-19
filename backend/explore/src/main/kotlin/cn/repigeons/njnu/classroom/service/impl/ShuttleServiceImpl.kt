package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsMapper
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.model.ShuttleRoute
import cn.repigeons.njnu.classroom.service.MailService
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.service.ShuttleService
import com.alibaba.fastjson.JSONArray
import com.google.gson.Gson
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.slf4j.LoggerFactory
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service
import org.springframework.web.multipart.MultipartFile
import java.io.File

@Service
open class ShuttleServiceImpl(
    private val gson: Gson,
    private val mailService: MailService,
    private val redisService: RedisService,
    private val shuttleMapper: ShuttleMapper,
    private val positionsMapper: PositionsMapper
) : ShuttleService {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Async
    override fun flushRoute() {
        Weekday.values().forEachIndexed { index, weekday ->
            val direction1 = JSONArray()
            val direction2 = JSONArray()
            val day = (1 shl 6 shr index).toByte()
            val route1 = shuttleMapper.selectRoute(day, 1)
            val route2 = shuttleMapper.selectRoute(day, 2)
            route1.forEach {
                val item = ShuttleRoute(
                    startTime = it.startTime!!,
                    startStation = it.startStation!!,
                    endStation = it.endStation!!
                )
                for (i in 1..it.shuttleCount!!)
                    direction1.add(item)
            }
            route2.forEach {
                val item = ShuttleRoute(
                    startTime = it.startTime!!,
                    startStation = it.startStation!!,
                    endStation = it.endStation!!
                )
                for (i in 1..it.shuttleCount!!)
                    direction2.add(item)
            }
            redisService["explore:shuttle:${weekday.value}:1"] = direction1.toJSONString()
            redisService["explore:shuttle:${weekday.value}:2"] = direction2.toJSONString()
        }
    }

    @Async
    override fun sendShuttleImage(file: MultipartFile) {
        logger.info("upload shuttle image: {}", file.originalFilename)
        val attachment = File.createTempFile(
            "shuttle_",
            ".${file.originalFilename?.split('.')?.lastOrNull()}"
        ).apply {
            file.transferTo(this)
            deleteOnExit()
        }
        logger.info("send shuttle image file: {}", attachment.name)
        mailService.send(
            subject = "【南师教室】有人上传校车时刻表.${file.originalFilename?.split('.')?.lastOrNull()}",
            content = "",
            attachment
        )
    }

    @Async
    override fun flushStationPosition() {
        val positions = positionsMapper.select {
            where(PositionsDynamicSqlSupport.Positions.kind, isEqualTo(2))
        }.map { record ->
            mapOf(
                Pair("name", record.name),
                Pair("position", listOf(record.latitude, record.longitude))
            )
        }
        redisService["static:position:shuttleStation"] = gson.toJson(positions)
    }

    override fun getStationPosition(): List<*> = gson.fromJson(
        redisService["static:position:shuttleStation"], List::class.java
    )
}