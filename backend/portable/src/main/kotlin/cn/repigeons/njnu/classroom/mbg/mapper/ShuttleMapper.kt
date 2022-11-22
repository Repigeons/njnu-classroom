/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:20.025+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.ShuttleRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface ShuttleMapper {
    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    fun count(selectStatement: SelectStatementProvider): Long

    @DeleteProvider(type=SqlProviderAdapter::class, method="delete")
    fun delete(deleteStatement: DeleteStatementProvider): Int

    @InsertProvider(type=SqlProviderAdapter::class, method="insert")
    @SelectKey(statement=["SELECT LAST_INSERT_ID()"], keyProperty="record.id", before=false, resultType=Int::class)
    fun insert(insertStatement: InsertStatementProvider<ShuttleRecord>): Int

    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    @ResultMap("ShuttleRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): ShuttleRecord?

    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    @Results(id="ShuttleRecordResult", value = [
        Result(column="id", property="id", jdbcType=JdbcType.INTEGER, id=true),
        Result(column="route", property="route", jdbcType=JdbcType.SMALLINT),
        Result(column="start_time", property="startTime", jdbcType=JdbcType.VARCHAR),
        Result(column="start_station", property="startStation", jdbcType=JdbcType.VARCHAR),
        Result(column="end_station", property="endStation", jdbcType=JdbcType.VARCHAR),
        Result(column="shuttle_count", property="shuttleCount", jdbcType=JdbcType.INTEGER),
        Result(column="working", property="working", jdbcType=JdbcType.CHAR)
    ])
    fun selectMany(selectStatement: SelectStatementProvider): List<ShuttleRecord>

    @UpdateProvider(type=SqlProviderAdapter::class, method="update")
    fun update(updateStatement: UpdateStatementProvider): Int
}