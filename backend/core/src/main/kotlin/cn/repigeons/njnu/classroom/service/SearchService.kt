package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Weekday

interface SearchService {
    fun search(
        jcKs: Short,
        jcJs: Short,
        day: Weekday?,
        jxl: String?,
        keyword: String?,
        page: Int,
        size: Int
    ): JsonResponse
}