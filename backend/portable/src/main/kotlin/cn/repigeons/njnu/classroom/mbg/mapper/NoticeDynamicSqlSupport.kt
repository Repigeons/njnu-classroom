/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-15T00:23:27.343+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType
import java.util.*

object NoticeDynamicSqlSupport {
    object Notice : SqlTable("notice") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val time = column<Date>("time", JDBCType.TIMESTAMP)

        val text = column<String>("text", JDBCType.VARCHAR)
    }
}