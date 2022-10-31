/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.513+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackDynamicSqlSupport.Feedback
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackDynamicSqlSupport.Feedback.id
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackDynamicSqlSupport.Feedback.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackDynamicSqlSupport.Feedback.jc
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackDynamicSqlSupport.Feedback.time
import cn.repigeons.njnu.classroom.mbg.model.FeedbackRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun FeedbackMapper.count(completer: CountCompleter) =
    countFrom(this::count, Feedback, completer)

fun FeedbackMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Feedback, completer)

fun FeedbackMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun FeedbackMapper.insert(record: FeedbackRecord) =
    insert(this::insert, record, Feedback) {
        map(time).toProperty("time")
        map(jc).toProperty("jc")
        map(jasdm).toProperty("jasdm")
    }

fun FeedbackMapper.insertSelective(record: FeedbackRecord) =
    insert(this::insert, record, Feedback) {
        map(time).toPropertyWhenPresent("time", record::time)
        map(jc).toPropertyWhenPresent("jc", record::jc)
        map(jasdm).toPropertyWhenPresent("jasdm", record::jasdm)
    }

private val columnList = listOf(id, time, jc, jasdm)

fun FeedbackMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Feedback, completer)

fun FeedbackMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Feedback, completer)

fun FeedbackMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Feedback, completer)

fun FeedbackMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun FeedbackMapper.update(completer: UpdateCompleter) =
    update(this::update, Feedback, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: FeedbackRecord) =
    apply {
        set(time).equalTo(record::time)
        set(jc).equalTo(record::jc)
        set(jasdm).equalTo(record::jasdm)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: FeedbackRecord) =
    apply {
        set(time).equalToWhenPresent(record::time)
        set(jc).equalToWhenPresent(record::jc)
        set(jasdm).equalToWhenPresent(record::jasdm)
    }

fun FeedbackMapper.updateByPrimaryKey(record: FeedbackRecord) =
    update {
        set(time).equalTo(record::time)
        set(jc).equalTo(record::jc)
        set(jasdm).equalTo(record::jasdm)
        where(id, isEqualTo(record::id))
    }

fun FeedbackMapper.updateByPrimaryKeySelective(record: FeedbackRecord) =
    update {
        set(time).equalToWhenPresent(record::time)
        set(jc).equalToWhenPresent(record::jc)
        set(jasdm).equalToWhenPresent(record::jasdm)
        where(id, isEqualTo(record::id))
    }