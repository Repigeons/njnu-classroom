package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.service.SpiderService
import cn.repigeons.njnu.classroom.util.GsonUtil
import cn.repigeons.njnu.classroom.util.ResourceUtil
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component

@Component
class Resources(
    cacheService: CacheService,
    spiderService: SpiderService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    val zylxdm = GsonUtil.fromJson(ResourceUtil.loadResourceText("/zylxdm.json")!!, List::class.java)

    init {
        spiderService.flushCache()
        cacheService.flushClassroomList()
        cacheService.flushBuildingPosition()
        logger.info("zylxdm.json={}", zylxdm)
    }
}