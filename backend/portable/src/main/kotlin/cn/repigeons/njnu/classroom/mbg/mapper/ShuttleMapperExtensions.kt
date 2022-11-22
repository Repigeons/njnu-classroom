/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:20.026+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.endStation
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.id
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.route
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.shuttleCount
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.startStation
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.startTime
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.working
import cn.repigeons.njnu.classroom.mbg.model.ShuttleRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun ShuttleMapper.count(completer: CountCompleter) =
    countFrom(this::count, Shuttle, completer)

fun ShuttleMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Shuttle, completer)

fun ShuttleMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun ShuttleMapper.insert(record: ShuttleRecord) =
    insert(this::insert, record, Shuttle) {
        map(route).toProperty("route")
        map(startTime).toProperty("startTime")
        map(startStation).toProperty("startStation")
        map(endStation).toProperty("endStation")
        map(shuttleCount).toProperty("shuttleCount")
        map(working).toProperty("working")
    }

fun ShuttleMapper.insertSelective(record: ShuttleRecord) =
    insert(this::insert, record, Shuttle) {
        map(route).toPropertyWhenPresent("route", record::route)
        map(startTime).toPropertyWhenPresent("startTime", record::startTime)
        map(startStation).toPropertyWhenPresent("startStation", record::startStation)
        map(endStation).toPropertyWhenPresent("endStation", record::endStation)
        map(shuttleCount).toPropertyWhenPresent("shuttleCount", record::shuttleCount)
        map(working).toPropertyWhenPresent("working", record::working)
    }

private val columnList = listOf(id, route, startTime, startStation, endStation, shuttleCount, working)

fun ShuttleMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Shuttle, completer)

fun ShuttleMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Shuttle, completer)

fun ShuttleMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Shuttle, completer)

fun ShuttleMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun ShuttleMapper.update(completer: UpdateCompleter) =
    update(this::update, Shuttle, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: ShuttleRecord) =
    apply {
        set(route).equalTo(record::route)
        set(startTime).equalTo(record::startTime)
        set(startStation).equalTo(record::startStation)
        set(endStation).equalTo(record::endStation)
        set(shuttleCount).equalTo(record::shuttleCount)
        set(working).equalTo(record::working)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: ShuttleRecord) =
    apply {
        set(route).equalToWhenPresent(record::route)
        set(startTime).equalToWhenPresent(record::startTime)
        set(startStation).equalToWhenPresent(record::startStation)
        set(endStation).equalToWhenPresent(record::endStation)
        set(shuttleCount).equalToWhenPresent(record::shuttleCount)
        set(working).equalToWhenPresent(record::working)
    }

fun ShuttleMapper.updateByPrimaryKey(record: ShuttleRecord) =
    update {
        set(route).equalTo(record::route)
        set(startTime).equalTo(record::startTime)
        set(startStation).equalTo(record::startStation)
        set(endStation).equalTo(record::endStation)
        set(shuttleCount).equalTo(record::shuttleCount)
        set(working).equalTo(record::working)
        where(id, isEqualTo(record::id))
    }

fun ShuttleMapper.updateByPrimaryKeySelective(record: ShuttleRecord) =
    update {
        set(route).equalToWhenPresent(record::route)
        set(startTime).equalToWhenPresent(record::startTime)
        set(startStation).equalToWhenPresent(record::startStation)
        set(endStation).equalToWhenPresent(record::endStation)
        set(shuttleCount).equalToWhenPresent(record::shuttleCount)
        set(working).equalToWhenPresent(record::working)
        where(id, isEqualTo(record::id))
    }