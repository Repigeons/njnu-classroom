package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.JsonResponse

interface OverviewService {
    fun getOverview(jasdm: String): JsonResponse
}