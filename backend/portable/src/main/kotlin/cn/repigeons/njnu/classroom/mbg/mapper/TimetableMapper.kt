/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:20.006+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.TimetableRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface TimetableMapper {
    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    fun count(selectStatement: SelectStatementProvider): Long

    @DeleteProvider(type=SqlProviderAdapter::class, method="delete")
    fun delete(deleteStatement: DeleteStatementProvider): Int

    @InsertProvider(type=SqlProviderAdapter::class, method="insert")
    @SelectKey(statement=["SELECT LAST_INSERT_ID()"], keyProperty="record.id", before=false, resultType=Int::class)
    fun insert(insertStatement: InsertStatementProvider<TimetableRecord>): Int

    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    @ResultMap("TimetableRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): TimetableRecord?

    @SelectProvider(type=SqlProviderAdapter::class, method="select")
    @Results(id="TimetableRecordResult", value = [
        Result(column="id", property="id", jdbcType=JdbcType.INTEGER, id=true),
        Result(column="JXLMC", property="jxlmc", jdbcType=JdbcType.VARCHAR),
        Result(column="jsmph", property="jsmph", jdbcType=JdbcType.VARCHAR),
        Result(column="JASDM", property="jasdm", jdbcType=JdbcType.CHAR),
        Result(column="SKZWS", property="skzws", jdbcType=JdbcType.INTEGER),
        Result(column="zylxdm", property="zylxdm", jdbcType=JdbcType.CHAR),
        Result(column="jc_ks", property="jcKs", jdbcType=JdbcType.SMALLINT),
        Result(column="jc_js", property="jcJs", jdbcType=JdbcType.SMALLINT),
        Result(column="weekday", property="weekday", jdbcType=JdbcType.VARCHAR),
        Result(column="SFYXZX", property="sfyxzx", jdbcType=JdbcType.BIT),
        Result(column="jyytms", property="jyytms", jdbcType=JdbcType.LONGVARCHAR),
        Result(column="kcm", property="kcm", jdbcType=JdbcType.LONGVARCHAR)
    ])
    fun selectMany(selectStatement: SelectStatementProvider): List<TimetableRecord>

    @UpdateProvider(type=SqlProviderAdapter::class, method="update")
    fun update(updateStatement: UpdateStatementProvider): Int
}