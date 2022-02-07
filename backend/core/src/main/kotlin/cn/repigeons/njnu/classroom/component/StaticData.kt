package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.util.ResourceUtil
import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.JSONArray
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component

@Component
class StaticData {
    private val logger = LoggerFactory.getLogger(javaClass)

    val zylxdm: JSONArray = JSON.parseArray(ResourceUtil.loadResource("/zylxdm.json"))
    val buildingPosition: JSONArray = JSON.parseArray(ResourceUtil.loadResource("/building_position.json"))

    init {
        logger.info("zylxdm.json={}", zylxdm)
        logger.info("building_position.json={}", buildingPosition)
    }
}