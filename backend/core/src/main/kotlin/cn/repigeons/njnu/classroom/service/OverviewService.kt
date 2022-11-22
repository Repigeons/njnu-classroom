package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.model.QueryResultItem

interface OverviewService {
    fun getOverview(jasdm: String): List<QueryResultItem>
}