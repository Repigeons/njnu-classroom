/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-15T19:29:10.795+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle
import cn.repigeons.njnu.classroom.mbg.mapper.ShuttleDynamicSqlSupport.Shuttle.endStation
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

fun ShuttleMapper.deleteByPrimaryKey(route_: Short, startTime_: String) =
    delete {
        where(route, isEqualTo(route_))
        and(startTime, isEqualTo(startTime_))
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

fun ShuttleMapper.insertMultiple(records: Collection<ShuttleRecord>) =
    insertMultiple(this::insertMultiple, records, Shuttle) {
        map(route).toProperty("route")
        map(startTime).toProperty("startTime")
        map(startStation).toProperty("startStation")
        map(endStation).toProperty("endStation")
        map(shuttleCount).toProperty("shuttleCount")
        map(working).toProperty("working")
    }

fun ShuttleMapper.insertMultiple(vararg records: ShuttleRecord) =
    insertMultiple(records.toList())

fun ShuttleMapper.insertSelective(record: ShuttleRecord) =
    insert(this::insert, record, Shuttle) {
        map(route).toPropertyWhenPresent("route", record::route)
        map(startTime).toPropertyWhenPresent("startTime", record::startTime)
        map(startStation).toPropertyWhenPresent("startStation", record::startStation)
        map(endStation).toPropertyWhenPresent("endStation", record::endStation)
        map(shuttleCount).toPropertyWhenPresent("shuttleCount", record::shuttleCount)
        map(working).toPropertyWhenPresent("working", record::working)
    }

private val columnList = listOf(route, startTime, startStation, endStation, shuttleCount, working)

fun ShuttleMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Shuttle, completer)

fun ShuttleMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Shuttle, completer)

fun ShuttleMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Shuttle, completer)

fun ShuttleMapper.selectByPrimaryKey(route_: Short, startTime_: String) =
    selectOne {
        where(route, isEqualTo(route_))
        and(startTime, isEqualTo(startTime_))
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
        set(startStation).equalTo(record::startStation)
        set(endStation).equalTo(record::endStation)
        set(shuttleCount).equalTo(record::shuttleCount)
        set(working).equalTo(record::working)
        where(route, isEqualTo(record::route))
        and(startTime, isEqualTo(record::startTime))
    }

fun ShuttleMapper.updateByPrimaryKeySelective(record: ShuttleRecord) =
    update {
        set(startStation).equalToWhenPresent(record::startStation)
        set(endStation).equalToWhenPresent(record::endStation)
        set(shuttleCount).equalToWhenPresent(record::shuttleCount)
        set(working).equalToWhenPresent(record::working)
        where(route, isEqualTo(record::route))
        and(startTime, isEqualTo(record::startTime))
    }