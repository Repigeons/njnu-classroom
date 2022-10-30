package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.mbg.mapper.JasMapper
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.RedisService
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.springframework.scheduling.annotation.Async
import org.springframework.stereotype.Service

@Service
open class CacheServiceImpl(
    private val redisService: RedisService,
    private val jasMapper: JasMapper,
    private val positionsMapper: PositionsMapper
) : CacheService {
    @Async
    override fun flushClassroomList() {
        val classrooms = jasMapper.select {}
            .map {
                mapOf(
                    Pair("jxlmc", it.jxldmDisplay),
                    Pair("jsmph", it.jasmc?.replace(Regex("^${it.jxldmDisplay}"), "")?.trim()),
                    Pair("jasdm", it.jasdm)
                )
            }
            .groupBy { it["jxlmc"]!! }
        redisService["static:classrooms"] = classrooms
    }

    override fun getClassroomList(): Map<*, *> = redisService["static:classrooms"]!!

    @Async
    override fun flushBuildingPosition() {
        val positions = positionsMapper.select {
            where(PositionsDynamicSqlSupport.Positions.kind, isEqualTo(1))
        }.map {
            mapOf(
                Pair("name", it.name),
                Pair("position", listOf(it.latitude, it.longitude))
            )
        }
        redisService["static:position:building"] = positions
    }

    override fun getBuildingPosition(): List<*> = redisService["static:position:building"]!!
}