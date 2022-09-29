/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-09-22T23:33:05.786228+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.FeedbackRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface FeedbackMapper {
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
    fun insert(insertStatement: InsertStatementProvider<FeedbackRecord>): Int

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @ResultMap("FeedbackRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): FeedbackRecord?

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @Results(
        id = "FeedbackRecordResult", value = [
            Result(column = "id", property = "id", jdbcType = JdbcType.INTEGER, id = true),
            Result(column = "time", property = "time", jdbcType = JdbcType.TIMESTAMP),
            Result(column = "jc", property = "jc", jdbcType = JdbcType.SMALLINT),
            Result(column = "JASDM", property = "jasdm", jdbcType = JdbcType.CHAR)
        ]
    )
    fun selectMany(selectStatement: SelectStatementProvider): List<FeedbackRecord>

    @UpdateProvider(type = SqlProviderAdapter::class, method = "update")
    fun update(updateStatement: UpdateStatementProvider): Int

    @Select(
        """ SELECT COUNT(0)                      AS `count`,
                   DATE_FORMAT(time, '%Y-%m-%d') AS `date` 
            FROM `feedback`
            WHERE `JASDM` = #{jasdm}
            AND DAYOFWEEK(time) = #{day_of_week}
            AND `jc` = #{jc}
            GROUP BY `date`
            ORDER BY `date`
        """
    )
    fun statistic(
        @Param("jasdm") jasdm: String,
        @Param("day_of_week") dayOfWeek: Int,
        @Param("jc") jc: Short
    ): List<Long>
}