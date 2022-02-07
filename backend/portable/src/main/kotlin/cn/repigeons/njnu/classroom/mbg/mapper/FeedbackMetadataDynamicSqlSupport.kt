/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-13T01:36:08.482+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import org.mybatis.dynamic.sql.SqlTable
import java.sql.JDBCType
import java.util.*

object FeedbackMetadataDynamicSqlSupport {
    object FeedbackMetadata : SqlTable("feedback_metadata") {
        val id = column<Int>("id", JDBCType.INTEGER)

        val time = column<Date>("time", JDBCType.TIMESTAMP)

        val jc = column<Short>("jc", JDBCType.SMALLINT)

        val jasdm = column<String>("JASDM", JDBCType.CHAR)
    }
}