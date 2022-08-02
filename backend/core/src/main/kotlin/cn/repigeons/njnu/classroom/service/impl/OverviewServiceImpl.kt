package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.model.QueryResultItem
import cn.repigeons.njnu.classroom.service.OverviewService
import cn.repigeons.njnu.classroom.util.GsonUtil
import org.redisson.api.RedissonClient
import org.springframework.stereotype.Service

@Service
class OverviewServiceImpl(
    private val redissonClient: RedissonClient
) : OverviewService {
    override fun getOverview(jasdm: String): JsonResponse {
        val rMap = redissonClient.getMap<String, String>("overview")
        val result = rMap[jasdm]?.let {
            GsonUtil.fromJson<List<QueryResultItem>>(it)
        } ?: return JsonResponse(
            status = Status.BAD_REQUEST,
            message = "无效参数: [jasdm]"
        )
        return JsonResponse(data = result)
    }
}