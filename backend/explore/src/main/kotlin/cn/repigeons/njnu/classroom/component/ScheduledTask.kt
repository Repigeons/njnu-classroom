package cn.repigeons.njnu.classroom.component

import cn.repigeons.njnu.classroom.common.Weekday
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleMapper
import cn.repigeons.njnu.classroom.model.ShuttleRoute
import cn.repigeons.njnu.classroom.service.RedisService
import com.alibaba.fastjson.JSONArray
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Component
import kotlin.concurrent.thread

@Component
class ScheduledTask(
    private val redisService: RedisService,
    private val shuttleMapper: ShuttleMapper
) {
    init {
        thread {
            flushShuttleLine()
        }
    }

    @Scheduled(cron = "0 0 6 * * *")
    fun flushShuttleLine() {
        Weekday.values().forEachIndexed { index, weekday ->
            val direction1 = JSONArray()
            val direction2 = JSONArray()
            val day = (1 shl 6 shr index).toByte()
            val route1 = shuttleMapper.selectRoute(day, 1)
            val route2 = shuttleMapper.selectRoute(day, 2)
            route1.forEach {
                val item = ShuttleRoute(
                    startTime = it.startTime!!,
                    startStation = it.startStation!!,
                    endStation = it.endStation!!
                )
                for (i in 1..it.shuttleCount!!)
                    direction1.add(item)
            }
            route2.forEach {
                val item = ShuttleRoute(
                    startTime = it.startTime!!,
                    startStation = it.startStation!!,
                    endStation = it.endStation!!
                )
                for (i in 1..it.shuttleCount!!)
                    direction2.add(item)
            }
            redisService["explore:shuttle:${weekday.value}:1"] = direction1.toJSONString()
            redisService["explore:shuttle:${weekday.value}:2"] = direction2.toJSONString()
        }
    }
}