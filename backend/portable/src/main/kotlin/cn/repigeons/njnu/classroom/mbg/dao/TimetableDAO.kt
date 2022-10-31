package cn.repigeons.njnu.classroom.mbg.dao

import org.apache.ibatis.annotations.Insert
import org.apache.ibatis.annotations.Mapper
import org.apache.ibatis.annotations.Update

@Mapper
interface TimetableDAO {
    @Update("TRUNCATE TABLE `timetable`")
    fun truncate()

    @Insert("INSERT INTO `timetable` SELECT * FROM `KCB`")
    fun cloneFromKcb()
}