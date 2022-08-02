package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.GridsMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.service.GridsService
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.util.GsonUtil
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.springframework.stereotype.Service

@Service
class GridsServiceImpl(
    private val redisService: RedisService,
    private val gridsMapper: GridsMapper
) : GridsService {
    override fun flushGrids() {
        val grids = gridsMapper.select {
            where(GridsDynamicSqlSupport.Grids.active, isEqualTo(true))
        }.map { record ->
            mapOf(
                Pair("text", record.text),
                Pair("imgUrl", record.imgUrl),
                Pair("url", record.url),
                Pair("method", record.method),
                Pair("button", record.button?.let { GsonUtil.fromJson(it, Map::class.java) })
            )
        }
        redisService["static:grids"] = GsonUtil.toJson(grids)
    }

    override fun getGrids(): List<*> = GsonUtil.fromJson(
        redisService["static:grids"]!!, List::class.java
    )
}