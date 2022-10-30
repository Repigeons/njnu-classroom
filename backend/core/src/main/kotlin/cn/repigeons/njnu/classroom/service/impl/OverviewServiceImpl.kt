package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.OverviewService
import cn.repigeons.njnu.classroom.service.RedisService
import org.springframework.stereotype.Service

@Service
class OverviewServiceImpl(
    private val redisService: RedisService
) : OverviewService {
    override fun getOverview(jasdm: String): JsonResponse {
        val result = requireNotNull(redisService.hGet<List<QueryResultItem>>("overview", jasdm)) {
            "无效参数: [jasdm]"
        }
        return JsonResponse(data = result)
    }
}