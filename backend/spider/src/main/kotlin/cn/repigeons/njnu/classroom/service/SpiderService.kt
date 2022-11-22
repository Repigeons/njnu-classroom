package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.enumerate.Weekday
import java.util.concurrent.Future

interface SpiderService {
    fun run(): Future<*>
    fun checkWithEhall(jasdm: String, weekday: Weekday, jc: Short, zylxdm: String): Boolean
}