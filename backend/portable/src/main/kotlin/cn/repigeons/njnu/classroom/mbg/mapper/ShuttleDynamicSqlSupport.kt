/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:20.024+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType

object ShuttleDynamicSqlSupport {
    object Shuttle : SqlTable("shuttle") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val route = column<Short>("route", JDBCType.SMALLINT)

        val startTime = column<String>("start_time", JDBCType.VARCHAR)

        val startStation = column<String>("start_station", JDBCType.VARCHAR)

        val endStation = column<String>("end_station", JDBCType.VARCHAR)

        val shuttleCount = column<Int>("shuttle_count", JDBCType.INTEGER)

        val working = column<String>("working", JDBCType.CHAR)
    }
}