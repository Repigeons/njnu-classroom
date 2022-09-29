package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsMapper
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.model.ShuttleRoute
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.service.ShuttleService
import cn.repigeons.njnu.classroom.util.EmailUtil
import cn.repigeons.njnu.classroom.util.GsonUtil
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service
import java.io.File

@Service
open class ShuttleServiceImpl(
    private val redisService: RedisService,
    private val shuttleMapper: ShuttleMapper,
    private val positionsMapper: PositionsMapper,
    @Value("\${spring.mail.receivers}")
    val receivers: Array<String>
) : ShuttleService {
    private val logger = LoggerFactory.getLogger(javaClass)

    @Async
    override fun flushRoute() {
        Weekday.values().forEachIndexed { index, weekday ->
            val direction1 = mutableListOf<ShuttleRoute>()
            val direction2 = mutableListOf<ShuttleRoute>()
            val day = if (index > 0) index else 7
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
            redisService["explore:shuttle:${weekday.value}:1"] = GsonUtil.toJson(direction1)
            redisService["explore:shuttle:${weekday.value}:2"] = GsonUtil.toJson(direction2)
        }
    }

    @Async
    override fun sendShuttleImage(filename: String?, bytes: ByteArray) {
        logger.info("upload shuttle image: {}", filename)
        val extension = filename?.split('.')?.lastOrNull()
        val attachment = File.createTempFile("shuttle_", extension).apply {
            deleteOnExit()
            outputStream().use { it.write(bytes) }
        }
        logger.info("send shuttle image file: {}", attachment.name)
        EmailUtil.sendFile(
            nickname = "南师教室",
            subject = "【南师教室】有人上传校车时刻表.${extension}",
            content = "",
            receivers = receivers,
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
        redisService["static:position:shuttleStation"] = GsonUtil.toJson(positions)
    }

    override fun getStationPosition() = GsonUtil.fromJson(
        redisService["static:position:shuttleStation"]!!, List::class.java
    )
}