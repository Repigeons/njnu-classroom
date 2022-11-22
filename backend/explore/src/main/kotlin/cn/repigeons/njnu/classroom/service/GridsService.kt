package cn.repigeons.njnu.classroom.service

import java.util.concurrent.Future

interface GridsService {
    fun flushGrids(): Future<*>
    fun getGrids(): List<*>
}