/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.346+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.JasRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface JasMapper {
    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    fun count(selectStatement: SelectStatementProvider): Long

    @DeleteProvider(type = SqlProviderAdapter::class, method = "delete")
    fun delete(deleteStatement: DeleteStatementProvider): Int

    @InsertProvider(type = SqlProviderAdapter::class, method = "insert")
    @SelectKey(
        statement = ["SELECT LAST_INSERT_ID()"],
        keyProperty = "record.jasdm",
        before = false,
        resultType = String::class
    )
    fun insert(insertStatement: InsertStatementProvider<JasRecord>): Int

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @ResultMap("JasRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): JasRecord?

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @Results(
        id = "JasRecordResult", value = [
            Result(column = "JASDM", property = "jasdm", jdbcType = JdbcType.CHAR, id = true),
            Result(column = "JASMC", property = "jasmc", jdbcType = JdbcType.VARCHAR),
            Result(column = "JXLDM", property = "jxldm", jdbcType = JdbcType.VARCHAR),
            Result(column = "JXLDM_DISPLAY", property = "jxldmDisplay", jdbcType = JdbcType.VARCHAR),
            Result(column = "XXXQDM", property = "xxxqdm", jdbcType = JdbcType.VARCHAR),
            Result(column = "XXXQDM_DISPLAY", property = "xxxqdmDisplay", jdbcType = JdbcType.VARCHAR),
            Result(column = "JASLXDM", property = "jaslxdm", jdbcType = JdbcType.VARCHAR),
            Result(column = "JASLXDM_DISPLAY", property = "jaslxdmDisplay", jdbcType = JdbcType.VARCHAR),
            Result(column = "ZT", property = "zt", jdbcType = JdbcType.VARCHAR),
            Result(column = "LC", property = "lc", jdbcType = JdbcType.SMALLINT),
            Result(column = "SKZWS", property = "skzws", jdbcType = JdbcType.INTEGER),
            Result(column = "KSZWS", property = "kszws", jdbcType = JdbcType.INTEGER),
            Result(column = "XNXQDM", property = "xnxqdm", jdbcType = JdbcType.VARCHAR),
            Result(column = "XNXQDM2", property = "xnxqdm2", jdbcType = JdbcType.VARCHAR),
            Result(column = "DWDM", property = "dwdm", jdbcType = JdbcType.VARCHAR),
            Result(column = "DWDM_DISPLAY", property = "dwdmDisplay", jdbcType = JdbcType.VARCHAR),
            Result(column = "ZWSXDM", property = "zwsxdm", jdbcType = JdbcType.VARCHAR),
            Result(column = "SYRQ", property = "syrq", jdbcType = JdbcType.VARCHAR),
            Result(column = "SYSJ", property = "sysj", jdbcType = JdbcType.VARCHAR),
            Result(column = "SXLB", property = "sxlb", jdbcType = JdbcType.VARCHAR),
            Result(column = "SFYPK", property = "sfypk", jdbcType = JdbcType.BIT),
            Result(column = "SFYXPK", property = "sfyxpk", jdbcType = JdbcType.BIT),
            Result(column = "PKYXJ", property = "pkyxj", jdbcType = JdbcType.VARCHAR),
            Result(column = "SFKSWH", property = "sfkswh", jdbcType = JdbcType.BIT),
            Result(column = "SFYXKS", property = "sfyxks", jdbcType = JdbcType.BIT),
            Result(column = "KSYXJ", property = "ksyxj", jdbcType = JdbcType.VARCHAR),
            Result(column = "SFYXCX", property = "sfyxcx", jdbcType = JdbcType.BIT),
            Result(column = "SFYXJY", property = "sfyxjy", jdbcType = JdbcType.BIT),
            Result(column = "SFYXZX", property = "sfyxzx", jdbcType = JdbcType.BIT),
            Result(column = "JSYT", property = "jsyt", jdbcType = JdbcType.LONGVARCHAR),
            Result(column = "XGDD", property = "xgdd", jdbcType = JdbcType.LONGVARCHAR),
            Result(column = "BZ", property = "bz", jdbcType = JdbcType.LONGVARCHAR)
        ]
    )
    fun selectMany(selectStatement: SelectStatementProvider): List<JasRecord>

    @UpdateProvider(type = SqlProviderAdapter::class, method = "update")
    fun update(updateStatement: UpdateStatementProvider): Int
}