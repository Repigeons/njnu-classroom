/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.535+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.PositionsRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface PositionsMapper {
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
    fun insert(insertStatement: InsertStatementProvider<PositionsRecord>): Int

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @ResultMap("PositionsRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): PositionsRecord?

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @Results(
        id = "PositionsRecordResult", value = [
            Result(column = "id", property = "id", jdbcType = JdbcType.INTEGER, id = true),
            Result(column = "name", property = "name", jdbcType = JdbcType.VARCHAR),
            Result(column = "latitude", property = "latitude", jdbcType = JdbcType.REAL),
            Result(column = "longitude", property = "longitude", jdbcType = JdbcType.REAL),
            Result(column = "kind", property = "kind", jdbcType = JdbcType.SMALLINT)
        ]
    )
    fun selectMany(selectStatement: SelectStatementProvider): List<PositionsRecord>

    @UpdateProvider(type = SqlProviderAdapter::class, method = "update")
    fun update(updateStatement: UpdateStatementProvider): Int
}