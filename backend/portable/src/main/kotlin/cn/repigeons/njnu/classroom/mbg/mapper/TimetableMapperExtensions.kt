/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-10-31T13:24:44.503+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.id
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.jcJs
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.jcKs
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.jsmph
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.jxlmc
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.jyytms
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.kcm
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.sfyxzx
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.skzws
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.weekday
import cn.repigeons.njnu.classroom.mbg.mapper.TimetableDynamicSqlSupport.Timetable.zylxdm
import cn.repigeons.njnu.classroom.mbg.model.TimetableRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun TimetableMapper.count(completer: CountCompleter) =
    countFrom(this::count, Timetable, completer)

fun TimetableMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Timetable, completer)

fun TimetableMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun TimetableMapper.insert(record: TimetableRecord) =
    insert(this::insert, record, Timetable) {
        map(jxlmc).toProperty("jxlmc")
        map(jsmph).toProperty("jsmph")
        map(jasdm).toProperty("jasdm")
        map(skzws).toProperty("skzws")
        map(zylxdm).toProperty("zylxdm")
        map(jcKs).toProperty("jcKs")
        map(jcJs).toProperty("jcJs")
        map(weekday).toProperty("weekday")
        map(sfyxzx).toProperty("sfyxzx")
        map(jyytms).toProperty("jyytms")
        map(kcm).toProperty("kcm")
    }

fun TimetableMapper.insertSelective(record: TimetableRecord) =
    insert(this::insert, record, Timetable) {
        map(jxlmc).toPropertyWhenPresent("jxlmc", record::jxlmc)
        map(jsmph).toPropertyWhenPresent("jsmph", record::jsmph)
        map(jasdm).toPropertyWhenPresent("jasdm", record::jasdm)
        map(skzws).toPropertyWhenPresent("skzws", record::skzws)
        map(zylxdm).toPropertyWhenPresent("zylxdm", record::zylxdm)
        map(jcKs).toPropertyWhenPresent("jcKs", record::jcKs)
        map(jcJs).toPropertyWhenPresent("jcJs", record::jcJs)
        map(weekday).toPropertyWhenPresent("weekday", record::weekday)
        map(sfyxzx).toPropertyWhenPresent("sfyxzx", record::sfyxzx)
        map(jyytms).toPropertyWhenPresent("jyytms", record::jyytms)
        map(kcm).toPropertyWhenPresent("kcm", record::kcm)
    }

private val columnList = listOf(id, jxlmc, jsmph, jasdm, skzws, zylxdm, jcKs, jcJs, weekday, sfyxzx, jyytms, kcm)

fun TimetableMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Timetable, completer)

fun TimetableMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Timetable, completer)

fun TimetableMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Timetable, completer)

fun TimetableMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun TimetableMapper.update(completer: UpdateCompleter) =
    update(this::update, Timetable, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: TimetableRecord) =
    apply {
        set(jxlmc).equalTo(record::jxlmc)
        set(jsmph).equalTo(record::jsmph)
        set(jasdm).equalTo(record::jasdm)
        set(skzws).equalTo(record::skzws)
        set(zylxdm).equalTo(record::zylxdm)
        set(jcKs).equalTo(record::jcKs)
        set(jcJs).equalTo(record::jcJs)
        set(weekday).equalTo(record::weekday)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jyytms).equalTo(record::jyytms)
        set(kcm).equalTo(record::kcm)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: TimetableRecord) =
    apply {
        set(jxlmc).equalToWhenPresent(record::jxlmc)
        set(jsmph).equalToWhenPresent(record::jsmph)
        set(jasdm).equalToWhenPresent(record::jasdm)
        set(skzws).equalToWhenPresent(record::skzws)
        set(zylxdm).equalToWhenPresent(record::zylxdm)
        set(jcKs).equalToWhenPresent(record::jcKs)
        set(jcJs).equalToWhenPresent(record::jcJs)
        set(weekday).equalToWhenPresent(record::weekday)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jyytms).equalToWhenPresent(record::jyytms)
        set(kcm).equalToWhenPresent(record::kcm)
    }

fun TimetableMapper.updateByPrimaryKey(record: TimetableRecord) =
    update {
        set(jxlmc).equalTo(record::jxlmc)
        set(jsmph).equalTo(record::jsmph)
        set(jasdm).equalTo(record::jasdm)
        set(skzws).equalTo(record::skzws)
        set(zylxdm).equalTo(record::zylxdm)
        set(jcKs).equalTo(record::jcKs)
        set(jcJs).equalTo(record::jcJs)
        set(weekday).equalTo(record::weekday)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jyytms).equalTo(record::jyytms)
        set(kcm).equalTo(record::kcm)
        where(id, isEqualTo(record::id))
    }

fun TimetableMapper.updateByPrimaryKeySelective(record: TimetableRecord) =
    update {
        set(jxlmc).equalToWhenPresent(record::jxlmc)
        set(jsmph).equalToWhenPresent(record::jsmph)
        set(jasdm).equalToWhenPresent(record::jasdm)
        set(skzws).equalToWhenPresent(record::skzws)
        set(zylxdm).equalToWhenPresent(record::zylxdm)
        set(jcKs).equalToWhenPresent(record::jcKs)
        set(jcJs).equalToWhenPresent(record::jcJs)
        set(weekday).equalToWhenPresent(record::weekday)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jyytms).equalToWhenPresent(record::jyytms)
        set(kcm).equalToWhenPresent(record::kcm)
        where(id, isEqualTo(record::id))
    }