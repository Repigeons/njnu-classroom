/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-01T23:00:28.9416491+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable
import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable.id
import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable.jsjc
import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable.ksjc
import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable.openid
import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable.place
import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable.remark
import cn.repigeons.njnu.classroom.mbg.mapper.UserTimetableDynamicSqlSupport.UserTimetable.weekday
import cn.repigeons.njnu.classroom.mbg.model.UserTimetableRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun UserTimetableMapper.count(completer: CountCompleter) =
    countFrom(this::count, UserTimetable, completer)

fun UserTimetableMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, UserTimetable, completer)

fun UserTimetableMapper.deleteByPrimaryKey(id_: Long) =
    delete {
        where(id, isEqualTo(id_))
    }

fun UserTimetableMapper.insert(record: UserTimetableRecord) =
    insert(this::insert, record, UserTimetable) {
        map(openid).toProperty("openid")
        map(weekday).toProperty("weekday")
        map(ksjc).toProperty("ksjc")
        map(jsjc).toProperty("jsjc")
        map(place).toProperty("place")
        map(remark).toProperty("remark")
    }

fun UserTimetableMapper.insertSelective(record: UserTimetableRecord) =
    insert(this::insert, record, UserTimetable) {
        map(openid).toPropertyWhenPresent("openid", record::openid)
        map(weekday).toPropertyWhenPresent("weekday", record::weekday)
        map(ksjc).toPropertyWhenPresent("ksjc", record::ksjc)
        map(jsjc).toPropertyWhenPresent("jsjc", record::jsjc)
        map(place).toPropertyWhenPresent("place", record::place)
        map(remark).toPropertyWhenPresent("remark", record::remark)
    }

private val columnList = listOf(id, openid, weekday, ksjc, jsjc, place, remark)

fun UserTimetableMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, UserTimetable, completer)

fun UserTimetableMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, UserTimetable, completer)

fun UserTimetableMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, UserTimetable, completer)

fun UserTimetableMapper.selectByPrimaryKey(id_: Long) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun UserTimetableMapper.update(completer: UpdateCompleter) =
    update(this::update, UserTimetable, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: UserTimetableRecord) =
    apply {
        set(openid).equalTo(record::openid)
        set(weekday).equalTo(record::weekday)
        set(ksjc).equalTo(record::ksjc)
        set(jsjc).equalTo(record::jsjc)
        set(place).equalTo(record::place)
        set(remark).equalTo(record::remark)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: UserTimetableRecord) =
    apply {
        set(openid).equalToWhenPresent(record::openid)
        set(weekday).equalToWhenPresent(record::weekday)
        set(ksjc).equalToWhenPresent(record::ksjc)
        set(jsjc).equalToWhenPresent(record::jsjc)
        set(place).equalToWhenPresent(record::place)
        set(remark).equalToWhenPresent(record::remark)
    }

fun UserTimetableMapper.updateByPrimaryKey(record: UserTimetableRecord) =
    update {
        set(openid).equalTo(record::openid)
        set(weekday).equalTo(record::weekday)
        set(ksjc).equalTo(record::ksjc)
        set(jsjc).equalTo(record::jsjc)
        set(place).equalTo(record::place)
        set(remark).equalTo(record::remark)
        where(id, isEqualTo(record::id))
    }

fun UserTimetableMapper.updateByPrimaryKeySelective(record: UserTimetableRecord) =
    update {
        set(openid).equalToWhenPresent(record::openid)
        set(weekday).equalToWhenPresent(record::weekday)
        set(ksjc).equalToWhenPresent(record::ksjc)
        set(jsjc).equalToWhenPresent(record::jsjc)
        set(place).equalToWhenPresent(record::place)
        set(remark).equalToWhenPresent(record::remark)
        where(id, isEqualTo(record::id))
    }