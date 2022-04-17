/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-15T00:23:27.357+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.NoticeRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface NoticeMapper {
    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    fun count(selectStatement: SelectStatementProvider): Long

    @DeleteProvider(type = SqlProviderAdapter::class, method = "delete")
    fun delete(deleteStatement: DeleteStatementProvider): Int

    @InsertProvider(type = SqlProviderAdapter::class, method = "insert")
    @SelectKey(
        statement = ["SELECT LAST_INSERT_ID()"],
        keyProperty = "record.id",
        before = false,
        resultType = Int::class
    )
    fun insert(insertStatement: InsertStatementProvider<NoticeRecord>): Int

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @ResultMap("NoticeRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): NoticeRecord?

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @Results(
        id = "NoticeRecordResult", value = [
            Result(column = "id", property = "id", jdbcType = JdbcType.INTEGER, id = true),
            Result(column = "time", property = "time", jdbcType = JdbcType.TIMESTAMP),
            Result(column = "text", property = "text", jdbcType = JdbcType.VARCHAR)
        ]
    )
    fun selectMany(selectStatement: SelectStatementProvider): List<NoticeRecord>

    @UpdateProvider(type = SqlProviderAdapter::class, method = "update")
    fun update(updateStatement: UpdateStatementProvider): Int
}