package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport
import cn.repigeons.njnu.classroom.mbg.mapper.GridsMapper
import cn.repigeons.njnu.classroom.mbg.mapper.select
import cn.repigeons.njnu.classroom.service.GridsService
import cn.repigeons.njnu.classroom.service.RedisService
import com.google.gson.Gson
import org.mybatis.dynamic.sql.util.kotlin.elements.isEqualTo
import org.springframework.stereotype.Service

@Service
class GridsServiceImpl(
    private val gson: Gson,
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
                Pair("button", record.button.let { gson.fromJson(it, Map::class.java) })
            )
        }
        redisService["static:grids"] = gson.toJson(grids)
    }

    override fun getGrids(): List<*> = gson.fromJson(
        redisService["static:grids"], List::class.java
    )
}