/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.545+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType

object GridsDynamicSqlSupport {
    object Grids : SqlTable("grids") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val text = column<String>("text", JDBCType.VARCHAR)

        val imgUrl = column<String>("img_url", JDBCType.VARCHAR)

        val url = column<String>("url", JDBCType.VARCHAR)

        val method = column<String>("method", JDBCType.VARCHAR)

        val button = column<String>("button", JDBCType.VARCHAR)

        val active = column<Boolean>("active", JDBCType.BIT)
    }
}