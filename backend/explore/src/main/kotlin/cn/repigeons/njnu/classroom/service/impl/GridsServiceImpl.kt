package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.commons.redisTemplate.RedisService
import cn.repigeons.commons.utils.GsonUtils
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.GridsMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.service.GridsService
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.springframework.stereotype.Service
import java.util.concurrent.CompletableFuture

@Service
class GridsServiceImpl(
    private val redisService: RedisService,
    private val gridsMapper: GridsMapper
) : GridsService {
    override fun flushGrids(): CompletableFuture<*> = CompletableFuture.supplyAsync {
        val grids = gridsMapper.select {
            where(GridsDynamicSqlSupport.Grids.active, isEqualTo(true))
        }.map { record ->
            mapOf(
                Pair("text", record.text),
                Pair("imgUrl", record.imgUrl),
                Pair("url", record.url),
                Pair("method", record.method),
                Pair("button", record.button?.let { GsonUtils.fromJson<Map<*, *>>(it) })
            )
        }
        redisService["static:grids"] = grids
    }

    override fun getGrids() = redisService["static:grids"] as List<*>
}