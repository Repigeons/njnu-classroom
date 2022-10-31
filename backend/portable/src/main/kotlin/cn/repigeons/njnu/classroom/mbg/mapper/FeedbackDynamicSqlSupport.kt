/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.511+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType
import java.util.*

object FeedbackDynamicSqlSupport {
    object Feedback : SqlTable("feedback") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val time = column<Date>("time", JDBCType.TIMESTAMP)

        val jc = column<Short>("jc", JDBCType.SMALLINT)

        val jasdm = column<String>("JASDM", JDBCType.CHAR)
    }
}