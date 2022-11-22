package cn.repigeons.njnu.classroom.component

import cn.repigeons.commons.utils.GsonUtils
import cn.repigeons.njnu.classroom.service.CacheService
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component

@Component
class Resources(
    cacheService: CacheService
) {
    private val logger = LoggerFactory.getLogger(javaClass)

    final val zylxdm: List<*> =
        GsonUtils.fromJson(javaClass.getResourceAsStream("/zylxdm.json")!!.reader())

    init {
        cacheService.flushClassroomList()
        cacheService.flushBuildingPosition()
        logger.info("zylxdm.json={}", zylxdm)
    }
}