package cn.repigeons.njnu.classroom.service

interface GridsService {
    fun flushGrids()
    fun getGrids(): List<*>
}