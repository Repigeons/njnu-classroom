/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-09T16:02:51.369+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType

object ProDynamicSqlSupport {
    object Pro : SqlTable("pro") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val jxlmc = column<String>("JXLMC", JDBCType.VARCHAR)

        val jsmph = column<String>("jsmph", JDBCType.VARCHAR)

        val jasdm = column<String>("JASDM", JDBCType.CHAR)

        val skzws = column<Int>("SKZWS", JDBCType.INTEGER)

        val zylxdm = column<String>("zylxdm", JDBCType.CHAR)

        val jcKs = column<Short>("jc_ks", JDBCType.SMALLINT)

        val jcJs = column<Short>("jc_js", JDBCType.SMALLINT)

        val day = column<String>("day", JDBCType.VARCHAR)

        val sfyxzx = column<Boolean>("SFYXZX", JDBCType.BIT)

        val jyytms = column<String>("jyytms", JDBCType.LONGVARCHAR)

        val kcm = column<String>("kcm", JDBCType.LONGVARCHAR)
    }
}