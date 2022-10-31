/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.554+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids.active
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids.button
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids.id
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids.imgUrl
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids.method
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids.text
import cn.repigeons.njnu.classroom.mbg.mapper.GridsDynamicSqlSupport.Grids.url
import cn.repigeons.njnu.classroom.mbg.model.GridsRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun GridsMapper.count(completer: CountCompleter) =
    countFrom(this::count, Grids, completer)

fun GridsMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Grids, completer)

fun GridsMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun GridsMapper.insert(record: GridsRecord) =
    insert(this::insert, record, Grids) {
        map(text).toProperty("text")
        map(imgUrl).toProperty("imgUrl")
        map(url).toProperty("url")
        map(method).toProperty("method")
        map(button).toProperty("button")
        map(active).toProperty("active")
    }

fun GridsMapper.insertSelective(record: GridsRecord) =
    insert(this::insert, record, Grids) {
        map(text).toPropertyWhenPresent("text", record::text)
        map(imgUrl).toPropertyWhenPresent("imgUrl", record::imgUrl)
        map(url).toPropertyWhenPresent("url", record::url)
        map(method).toPropertyWhenPresent("method", record::method)
        map(button).toPropertyWhenPresent("button", record::button)
        map(active).toPropertyWhenPresent("active", record::active)
    }

private val columnList = listOf(id, text, imgUrl, url, method, button, active)

fun GridsMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Grids, completer)

fun GridsMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Grids, completer)

fun GridsMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Grids, completer)

fun GridsMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun GridsMapper.update(completer: UpdateCompleter) =
    update(this::update, Grids, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: GridsRecord) =
    apply {
        set(text).equalTo(record::text)
        set(imgUrl).equalTo(record::imgUrl)
        set(url).equalTo(record::url)
        set(method).equalTo(record::method)
        set(button).equalTo(record::button)
        set(active).equalTo(record::active)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: GridsRecord) =
    apply {
        set(text).equalToWhenPresent(record::text)
        set(imgUrl).equalToWhenPresent(record::imgUrl)
        set(url).equalToWhenPresent(record::url)
        set(method).equalToWhenPresent(record::method)
        set(button).equalToWhenPresent(record::button)
        set(active).equalToWhenPresent(record::active)
    }

fun GridsMapper.updateByPrimaryKey(record: GridsRecord) =
    update {
        set(text).equalTo(record::text)
        set(imgUrl).equalTo(record::imgUrl)
        set(url).equalTo(record::url)
        set(method).equalTo(record::method)
        set(button).equalTo(record::button)
        set(active).equalTo(record::active)
        where(id, isEqualTo(record::id))
    }

fun GridsMapper.updateByPrimaryKeySelective(record: GridsRecord) =
    update {
        set(text).equalToWhenPresent(record::text)
        set(imgUrl).equalToWhenPresent(record::imgUrl)
        set(url).equalToWhenPresent(record::url)
        set(method).equalToWhenPresent(record::method)
        set(button).equalToWhenPresent(record::button)
        set(active).equalToWhenPresent(record::active)
        where(id, isEqualTo(record::id))
    }