/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:20.017+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType

object CorrectionDynamicSqlSupport {
    object Correction : SqlTable("correction") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val weekday = column<String>("weekday", JDBCType.VARCHAR)

        val jxlmc = column<String>("JXLMC", JDBCType.VARCHAR)

        val jsmph = column<String>("jsmph", JDBCType.VARCHAR)

        val jasdm = column<String>("JASDM", JDBCType.VARCHAR)

        val skzws = column<Int>("SKZWS", JDBCType.INTEGER)

        val zylxdm = column<String>("zylxdm", JDBCType.VARCHAR)

        val jcKs = column<Short>("jc_ks", JDBCType.SMALLINT)

        val jcJs = column<Short>("jc_js", JDBCType.SMALLINT)

        val sfyxzx = column<Boolean>("SFYXZX", JDBCType.BIT)

        val jyytms = column<String>("jyytms", JDBCType.LONGVARCHAR)

        val kcm = column<String>("kcm", JDBCType.LONGVARCHAR)
    }
}