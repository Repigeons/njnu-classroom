/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-01T23:00:28.91165+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType

object UserTimetableDynamicSqlSupport {
    object UserTimetable : SqlTable("user_timetable") {
        val id = column<Long>("id", JDBCType.BIGINT)

        val openid = column<String>("openid", JDBCType.VARCHAR)

        val weekday = column<String>("weekday", JDBCType.VARCHAR)

        val ksjc = column<Short>("ksjc", JDBCType.SMALLINT)

        val jsjc = column<Short>("jsjc", JDBCType.SMALLINT)

        val place = column<String>("place", JDBCType.VARCHAR)

        val remark = column<String>("remark", JDBCType.LONGVARCHAR)
    }
}