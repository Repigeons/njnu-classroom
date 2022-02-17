package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.Weekday
import java.util.concurrent.Future

interface SpiderService {
    fun run(): Future<*>
    fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String): Boolean
}