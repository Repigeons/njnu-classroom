package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.Weekday
import org.redisson.api.RLock
import java.util.concurrent.Future

interface SpiderService {
    fun run(lock: RLock? = null): Future<*>
    fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String): Boolean
}