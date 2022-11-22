package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.commons.redisTemplate.RedisService
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.OverviewService
import org.springframework.stereotype.Service

@Service
class OverviewServiceImpl(
    private val redisService: RedisService
) : OverviewService {
    override fun getOverview(jasdm: String): List<QueryResultItem> =
        requireNotNull(redisService.hGet("overview", jasdm) as List<*>?) {
            "无效参数: [jasdm]"
        }.map { it as QueryResultItem }
}
