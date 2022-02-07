/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-13T01:36:08.491+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.model.FeedbackMetadataRecord
import org.apache.ibatis.annotations.*
import org.apache.ibatis.type.JdbcType
import org.mybatis.dynamic.sql.delete.render.DeleteStatementProvider
import org.mybatis.dynamic.sql.insert.render.InsertStatementProvider
import org.mybatis.dynamic.sql.select.render.SelectStatementProvider
import org.mybatis.dynamic.sql.update.render.UpdateStatementProvider
import org.mybatis.dynamic.sql.util.SqlProviderAdapter

@Mapper
interface FeedbackMetadataMapper {
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
    fun insert(insertStatement: InsertStatementProvider<FeedbackMetadataRecord>): Int

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @ResultMap("FeedbackMetadataRecordResult")
    fun selectOne(selectStatement: SelectStatementProvider): FeedbackMetadataRecord?

    @SelectProvider(type = SqlProviderAdapter::class, method = "select")
    @Results(
        id = "FeedbackMetadataRecordResult", value = [
            Result(column = "id", property = "id", jdbcType = JdbcType.INTEGER, id = true),
            Result(column = "time", property = "time", jdbcType = JdbcType.TIMESTAMP),
            Result(column = "jc", property = "jc", jdbcType = JdbcType.SMALLINT),
            Result(column = "JASDM", property = "jasdm", jdbcType = JdbcType.CHAR)
        ]
    )
    fun selectMany(selectStatement: SelectStatementProvider): List<FeedbackMetadataRecord>

    @UpdateProvider(type = SqlProviderAdapter::class, method = "update")
    fun update(updateStatement: UpdateStatementProvider): Int

    @Select(
        "SELECT COUNT(*) `count`, DATE_FORMAT(time, '%Y-%m-%d') `date` " +
                "FROM `feedback_metadata` " +
                "WHERE `JASDM`=#{jasdm} " +
                "AND DAYOFWEEK(time)=#{day_of_week} " +
                "AND `jc`=#{jc} " +
                "GROUP BY `date` " +
                "ORDER BY `date`"
    )
    fun statistic(
        @Param("jasdm") jasdm: String,
        @Param("day_of_week") dayOfWeek: Int,
        @Param("jc") jc: Short
    ): List<Long>
}