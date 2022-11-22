/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:20.023+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.NoticeDynamicSqlSupport.Notice
import cn.repigeons.njnu.classroom.mbg.mapper.NoticeDynamicSqlSupport.Notice.id
import cn.repigeons.njnu.classroom.mbg.mapper.NoticeDynamicSqlSupport.Notice.text
import cn.repigeons.njnu.classroom.mbg.mapper.NoticeDynamicSqlSupport.Notice.time
import cn.repigeons.njnu.classroom.mbg.model.NoticeRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun NoticeMapper.count(completer: CountCompleter) =
    countFrom(this::count, Notice, completer)

fun NoticeMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Notice, completer)

fun NoticeMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun NoticeMapper.insert(record: NoticeRecord) =
    insert(this::insert, record, Notice) {
        map(time).toProperty("time")
        map(text).toProperty("text")
    }

fun NoticeMapper.insertSelective(record: NoticeRecord) =
    insert(this::insert, record, Notice) {
        map(time).toPropertyWhenPresent("time", record::time)
        map(text).toPropertyWhenPresent("text", record::text)
    }

private val columnList = listOf(id, time, text)

fun NoticeMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Notice, completer)

fun NoticeMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Notice, completer)

fun NoticeMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Notice, completer)

fun NoticeMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun NoticeMapper.update(completer: UpdateCompleter) =
    update(this::update, Notice, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: NoticeRecord) =
    apply {
        set(time).equalTo(record::time)
        set(text).equalTo(record::text)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: NoticeRecord) =
    apply {
        set(time).equalToWhenPresent(record::time)
        set(text).equalToWhenPresent(record::text)
    }

fun NoticeMapper.updateByPrimaryKey(record: NoticeRecord) =
    update {
        set(time).equalTo(record::time)
        set(text).equalTo(record::text)
        where(id, isEqualTo(record::id))
    }

fun NoticeMapper.updateByPrimaryKeySelective(record: NoticeRecord) =
    update {
        set(time).equalToWhenPresent(record::time)
        set(text).equalToWhenPresent(record::text)
        where(id, isEqualTo(record::id))
    }