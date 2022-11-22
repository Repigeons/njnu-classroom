package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.commons.redisTemplate.RedisService
import cn.repigeons.njnu.classroom.mbg.mapper.JasMapper
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.service.CacheService
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.springframework.stereotype.Service
import java.util.concurrent.CompletableFuture

@Service
class CacheServiceImpl(
    private val redisService: RedisService,
    private val jasMapper: JasMapper,
    private val positionsMapper: PositionsMapper
) : CacheService {
    override fun flushClassroomList(): CompletableFuture<*> = CompletableFuture.supplyAsync {
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

    override fun getClassroomList() = redisService["static:classrooms"] as Map<*, *>

    override fun flushBuildingPosition(): CompletableFuture<*> = CompletableFuture.supplyAsync {
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

    override fun getBuildingPosition() = redisService["static:position:building"] as List<*>
}