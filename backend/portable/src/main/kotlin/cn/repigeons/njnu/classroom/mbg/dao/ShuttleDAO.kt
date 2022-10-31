package cn.repigeons.njnu.classroom.mbg.dao

import cn.repigeons.njnu.classroom.mbg.model.ShuttleRecord
import org.apache.ibatis.annotations.Mapper
import org.apache.ibatis.annotations.Param
import org.apache.ibatis.annotations.ResultMap
import org.apache.ibatis.annotations.Select

@Mapper
interface ShuttleDAO {
    @Select("SELECT * FROM `shuttle` WHERE SUBSTR(working,#{day},1)='1' AND route=#{route}")
    @ResultMap("ShuttleRecordResult")
    fun selectRoute(
        @Param("day") day: Int,
        @Param("route") route: Short
    ): List<ShuttleRecord>
}