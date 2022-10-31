/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.324+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType

object JasDynamicSqlSupport {
    object Jas : SqlTable("JAS") {
        val jasdm = column<String>("JASDM", JDBCType.CHAR)

        val jasmc = column<String>("JASMC", JDBCType.VARCHAR)

        val jxldm = column<String>("JXLDM", JDBCType.VARCHAR)

        val jxldmDisplay = column<String>("JXLDM_DISPLAY", JDBCType.VARCHAR)

        val xxxqdm = column<String>("XXXQDM", JDBCType.VARCHAR)

        val xxxqdmDisplay = column<String>("XXXQDM_DISPLAY", JDBCType.VARCHAR)

        val jaslxdm = column<String>("JASLXDM", JDBCType.VARCHAR)

        val jaslxdmDisplay = column<String>("JASLXDM_DISPLAY", JDBCType.VARCHAR)

        val zt = column<String>("ZT", JDBCType.VARCHAR)

        val lc = column<Short>("LC", JDBCType.SMALLINT)

        val skzws = column<Int>("SKZWS", JDBCType.INTEGER)

        val kszws = column<Int>("KSZWS", JDBCType.INTEGER)

        val xnxqdm = column<String>("XNXQDM", JDBCType.VARCHAR)

        val xnxqdm2 = column<String>("XNXQDM2", JDBCType.VARCHAR)

        val dwdm = column<String>("DWDM", JDBCType.VARCHAR)

        val dwdmDisplay = column<String>("DWDM_DISPLAY", JDBCType.VARCHAR)

        val zwsxdm = column<String>("ZWSXDM", JDBCType.VARCHAR)

        val syrq = column<String>("SYRQ", JDBCType.VARCHAR)

        val sysj = column<String>("SYSJ", JDBCType.VARCHAR)

        val sxlb = column<String>("SXLB", JDBCType.VARCHAR)

        val sfypk = column<Boolean>("SFYPK", JDBCType.BIT)

        val sfyxpk = column<Boolean>("SFYXPK", JDBCType.BIT)

        val pkyxj = column<String>("PKYXJ", JDBCType.VARCHAR)

        val sfkswh = column<Boolean>("SFKSWH", JDBCType.BIT)

        val sfyxks = column<Boolean>("SFYXKS", JDBCType.BIT)

        val ksyxj = column<String>("KSYXJ", JDBCType.VARCHAR)

        val sfyxcx = column<Boolean>("SFYXCX", JDBCType.BIT)

        val sfyxjy = column<Boolean>("SFYXJY", JDBCType.BIT)

        val sfyxzx = column<Boolean>("SFYXZX", JDBCType.BIT)

        val jsyt = column<String>("JSYT", JDBCType.LONGVARCHAR)

        val xgdd = column<String>("XGDD", JDBCType.LONGVARCHAR)

        val bz = column<String>("BZ", JDBCType.LONGVARCHAR)
    }
}