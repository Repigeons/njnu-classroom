package cn.repigeons.njnu.classroom.service

import cn.repigeons.njnu.classroom.common.Weekday

interface SpiderService {
    fun run()
    fun checkWithEhall(jasdm: String, day: Weekday, jc: Short, zylxdm: String): Boolean
}