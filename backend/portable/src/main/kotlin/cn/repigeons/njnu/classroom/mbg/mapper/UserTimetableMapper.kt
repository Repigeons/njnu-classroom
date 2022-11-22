/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:20.036+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.UserTimetableRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface UserTimetableMapper {
    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    fun count(selectStatement: SelectStatementProvider): Long

    @DeleteProvider(type=SqlProviderAdapter::class, method="delete")
    fun delete(deleteStatement: DeleteStatementProvider): Int

    @InsertProvider(type=SqlProviderAdapter::class, method="insert")
    @SelectKey(statement=["SELECT LAST_INSERT_ID()"], keyProperty="record.id", before=false, resultType=Long::class)
    fun insert(insertStatement: InsertStatementProvider<UserTimetableRecord>): Int

    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    @ResultMap("UserTimetableRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): UserTimetableRecord?

    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    @Results(id="UserTimetableRecordResult", value = [
        Result(column="id", property="id", jdbcType=JdbcType.BIGINT, id=true),
        Result(column="openid", property="openid", jdbcType=JdbcType.VARCHAR),
        Result(column="weekday", property="weekday", jdbcType=JdbcType.VARCHAR),
        Result(column="ksjc", property="ksjc", jdbcType=JdbcType.SMALLINT),
        Result(column="jsjc", property="jsjc", jdbcType=JdbcType.SMALLINT),
        Result(column="place", property="place", jdbcType=JdbcType.VARCHAR),
        Result(column="remark", property="remark", jdbcType=JdbcType.LONGVARCHAR)
    ])
    fun selectMany(selectStatement: SelectStatementProvider): List<UserTimetableRecord>

    @UpdateProvider(type=SqlProviderAdapter::class, method="update")
    fun update(updateStatement: UpdateStatementProvider): Int
}