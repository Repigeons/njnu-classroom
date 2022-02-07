package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.util.ResourceUtil
import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.JSONArray
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component

@Component
class StaticData {
    private val logger = LoggerFactory.getLogger(javaClass)

    val grids: JSONArray = JSON.parseArray(ResourceUtil.loadResource("/grids.json"))
    val shuttleStationPosition: JSONArray = JSON.parseArray(ResourceUtil.loadResource("/shuttle_station_position.json"))

    init {
        logger.info("grids.json={}", grids)
        logger.info("shuttle_station_position.json={}", shuttleStationPosition)
    }
}