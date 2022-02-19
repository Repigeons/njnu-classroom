/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-21T00:02:16.349+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.GridsRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface GridsMapper {
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
    fun insert(insertStatement: InsertStatementProvider<GridsRecord>): Int

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @ResultMap("GridsRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): GridsRecord?

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @Results(
        id = "GridsRecordResult", value = [
            Result(column = "id", property = "id", jdbcType = JdbcType.INTEGER, id = true),
            Result(column = "text", property = "text", jdbcType = JdbcType.VARCHAR),
            Result(column = "img_url", property = "imgUrl", jdbcType = JdbcType.VARCHAR),
            Result(column = "url", property = "url", jdbcType = JdbcType.VARCHAR),
            Result(column = "method", property = "method", jdbcType = JdbcType.VARCHAR),
            Result(column = "button", property = "button", jdbcType = JdbcType.VARCHAR),
            Result(column = "active", property = "active", jdbcType = JdbcType.BIT)
        ]
    )
    fun selectMany(selectStatement: SelectStatementProvider): List<GridsRecord>

    @UpdateProvider(type = SqlProviderAdapter::class, method = "update")
    fun update(updateStatement: UpdateStatementProvider): Int
}