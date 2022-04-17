/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-19T16:10:52.269+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType

object PositionsDynamicSqlSupport {
    object Positions : SqlTable("positions") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val name = column<String>("name", JDBCType.VARCHAR)

        val latitude = column<Float>("latitude", JDBCType.REAL)

        val longitude = column<Float>("longitude", JDBCType.REAL)

        val kind = column<Short>("kind", JDBCType.SMALLINT)
    }
}