package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.util.ResourceUtil
import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.JSONArray
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component
import kotlin.concurrent.thread

@Component
class Resources(
    private val cacheService: CacheService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    val zylxdm: JSONArray = JSON.parseArray(ResourceUtil.loadResource("/zylxdm.json"))

    init {
        thread { cacheService.flush() }
        thread { cacheService.flushClassroomList() }
        thread { cacheService.flushBuildingPosition() }
        logger.info("zylxdm.json={}", zylxdm)
    }
}