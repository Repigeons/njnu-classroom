package cn.repigeons.njnu.classroom.mbg.dao

import cn.repigeons.njnu.classroom.mbg.model.ShuttleRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType

@Mapper
interface ShuttleDAO {
    @Select("SELECT * FROM `shuttle` WHERE SUBSTR(working,#{day},1)='1' AND route=#{route}")
    @Results(
        id = "ShuttleRecordResult", value = [
            Result(column = "id", property = "id", jdbcType = JdbcType.INTEGER, id = true),
            Result(column = "route", property = "route", jdbcType = JdbcType.SMALLINT),
            Result(column = "start_time", property = "startTime", jdbcType = JdbcType.VARCHAR),
            Result(column = "start_station", property = "startStation", jdbcType = JdbcType.VARCHAR),
            Result(column = "end_station", property = "endStation", jdbcType = JdbcType.VARCHAR),
            Result(column = "shuttle_count", property = "shuttleCount", jdbcType = JdbcType.INTEGER),
            Result(column = "working", property = "working", jdbcType = JdbcType.CHAR)
        ]
    )
    fun selectRoute(
        @Param("day") day: Int,
        @Param("route") route: Short
    ): List<ShuttleRecord>
}