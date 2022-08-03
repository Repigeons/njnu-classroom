package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.service.CacheService
import cn.repigeons.njnu.classroom.util.GsonUtil
import cn.repigeons.njnu.classroom.util.ResourceUtil
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component
import kotlin.concurrent.thread

@Component
class Resources(
    private val cacheService: CacheService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    val zylxdm = GsonUtil.fromJson(ResourceUtil.loadResourceText("/zylxdm.json")!!, List::class.java)

    init {
        thread { cacheService.flush() }
        thread { cacheService.flushClassroomList() }
        thread { cacheService.flushBuildingPosition() }
        logger.info("zylxdm.json={}", zylxdm)
    }
}