/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-19T16:10:52.302+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport.Positions
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport.Positions.id
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport.Positions.kind
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport.Positions.latitude
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport.Positions.longitude
import cn.repigeons.njnu.classroom.mbg.mapper.PositionsDynamicSqlSupport.Positions.name
import cn.repigeons.njnu.classroom.mbg.model.PositionsRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun PositionsMapper.count(completer: CountCompleter) =
    countFrom(this::count, Positions, completer)

fun PositionsMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Positions, completer)

fun PositionsMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun PositionsMapper.insert(record: PositionsRecord) =
    insert(this::insert, record, Positions) {
        map(name).toProperty("name")
        map(latitude).toProperty("latitude")
        map(longitude).toProperty("longitude")
        map(kind).toProperty("kind")
    }

fun PositionsMapper.insertSelective(record: PositionsRecord) =
    insert(this::insert, record, Positions) {
        map(name).toPropertyWhenPresent("name", record::name)
        map(latitude).toPropertyWhenPresent("latitude", record::latitude)
        map(longitude).toPropertyWhenPresent("longitude", record::longitude)
        map(kind).toPropertyWhenPresent("kind", record::kind)
    }

private val columnList = listOf(id, name, latitude, longitude, kind)

fun PositionsMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Positions, completer)

fun PositionsMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Positions, completer)

fun PositionsMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Positions, completer)

fun PositionsMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun PositionsMapper.update(completer: UpdateCompleter) =
    update(this::update, Positions, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: PositionsRecord) =
    apply {
        set(name).equalTo(record::name)
        set(latitude).equalTo(record::latitude)
        set(longitude).equalTo(record::longitude)
        set(kind).equalTo(record::kind)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: PositionsRecord) =
    apply {
        set(name).equalToWhenPresent(record::name)
        set(latitude).equalToWhenPresent(record::latitude)
        set(longitude).equalToWhenPresent(record::longitude)
        set(kind).equalToWhenPresent(record::kind)
    }

fun PositionsMapper.updateByPrimaryKey(record: PositionsRecord) =
    update {
        set(name).equalTo(record::name)
        set(latitude).equalTo(record::latitude)
        set(longitude).equalTo(record::longitude)
        set(kind).equalTo(record::kind)
        where(id, isEqualTo(record::id))
    }

fun PositionsMapper.updateByPrimaryKeySelective(record: PositionsRecord) =
    update {
        set(name).equalToWhenPresent(record::name)
        set(latitude).equalToWhenPresent(record::latitude)
        set(longitude).equalToWhenPresent(record::longitude)
        set(kind).equalToWhenPresent(record::kind)
        where(id, isEqualTo(record::id))
    }