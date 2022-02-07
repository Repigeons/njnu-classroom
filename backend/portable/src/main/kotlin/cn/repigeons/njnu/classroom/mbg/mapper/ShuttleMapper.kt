/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-15T19:29:10.783+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.ShuttleRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.insert.render.MultiRowInsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface ShuttleMapper {
    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    fun count(selectStatement: SelectStatementProvider): Long

    @DeleteProvider(type = SqlProviderAdapter::class, method = "delete")
    fun delete(deleteStatement: DeleteStatementProvider): Int

    @InsertProvider(type = SqlProviderAdapter::class, method = "insert")
    fun insert(insertStatement: InsertStatementProvider<ShuttleRecord>): Int

    @InsertProvider(type = SqlProviderAdapter::class, method = "insertMultiple")
    fun insertMultiple(multipleInsertStatement: MultiRowInsertStatementProvider<ShuttleRecord>): Int

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @ResultMap("ShuttleRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): ShuttleRecord?

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @Results(
        id = "ShuttleRecordResult", value = [
            Result(column = "route", property = "route", jdbcType = JdbcType.SMALLINT, id = true),
            Result(column = "start_time", property = "startTime", jdbcType = JdbcType.VARCHAR, id = true),
            Result(column = "start_station", property = "startStation", jdbcType = JdbcType.VARCHAR),
            Result(column = "end_station", property = "endStation", jdbcType = JdbcType.VARCHAR),
            Result(column = "shuttle_count", property = "shuttleCount", jdbcType = JdbcType.INTEGER),
            Result(column = "working", property = "working", jdbcType = JdbcType.BIT)
        ]
    )
    fun selectMany(selectStatement: SelectStatementProvider): List<ShuttleRecord>

    @UpdateProvider(type = SqlProviderAdapter::class, method = "update")
    fun update(updateStatement: UpdateStatementProvider): Int

    @Select("SELECT * FROM `shuttle` WHERE (`working`& #{day}) AND `route`=#{route}")
    @ResultMap("ShuttleRecordResult")
    fun selectRoute(
        @Param("day") day: Byte,
        @Param("route") route: Short
    ): List<ShuttleRecord>
}