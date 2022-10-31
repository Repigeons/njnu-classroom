package cn.repigeons.njnu.classroom.mbg.dao

import org.apache.ibatis.annotations.Mapper
import org.apache.ibatis.annotations.Param
import org.apache.ibatis.annotations.Select

@Mapper
interface FeedbackDAO {
    @Select(
        """ SELECT COUNT(0)                      AS `count`,
                   DATE_FORMAT(time, '%Y-%m-%d') AS `date` 
            FROM `feedback`
            WHERE `JASDM` = #{jasdm}
            AND DAYOFWEEK(time) = #{day_of_week}
            AND `jc` = #{jc}
            GROUP BY `date`
            ORDER BY `date`
        """
    )
    fun statistic(
        @Param("jasdm") jasdm: String,
        @Param("day_of_week") dayOfWeek: Int,
        @Param("jc") jc: Short
    ): List<Long>
}