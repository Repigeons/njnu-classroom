/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-09T16:02:51.371+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.day
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.id
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.jcJs
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.jcKs
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.jsmph
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.jxlmc
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.jyytms
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.kcm
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.sfyxzx
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.skzws
import cn.repigeons.njnu.classroom.mbg.mapper.ProDynamicSqlSupport.Pro.zylxdm
import cn.repigeons.njnu.classroom.mbg.model.ProRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun ProMapper.count(completer: CountCompleter) =
    countFrom(this::count, Pro, completer)

fun ProMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Pro, completer)

fun ProMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun ProMapper.insert(record: ProRecord) =
    insert(this::insert, record, Pro) {
        map(jxlmc).toProperty("jxlmc")
        map(jsmph).toProperty("jsmph")
        map(jasdm).toProperty("jasdm")
        map(skzws).toProperty("skzws")
        map(zylxdm).toProperty("zylxdm")
        map(jcKs).toProperty("jcKs")
        map(jcJs).toProperty("jcJs")
        map(day).toProperty("day")
        map(sfyxzx).toProperty("sfyxzx")
        map(jyytms).toProperty("jyytms")
        map(kcm).toProperty("kcm")
    }

fun ProMapper.insertSelective(record: ProRecord) =
    insert(this::insert, record, Pro) {
        map(jxlmc).toPropertyWhenPresent("jxlmc", record::jxlmc)
        map(jsmph).toPropertyWhenPresent("jsmph", record::jsmph)
        map(jasdm).toPropertyWhenPresent("jasdm", record::jasdm)
        map(skzws).toPropertyWhenPresent("skzws", record::skzws)
        map(zylxdm).toPropertyWhenPresent("zylxdm", record::zylxdm)
        map(jcKs).toPropertyWhenPresent("jcKs", record::jcKs)
        map(jcJs).toPropertyWhenPresent("jcJs", record::jcJs)
        map(day).toPropertyWhenPresent("day", record::day)
        map(sfyxzx).toPropertyWhenPresent("sfyxzx", record::sfyxzx)
        map(jyytms).toPropertyWhenPresent("jyytms", record::jyytms)
        map(kcm).toPropertyWhenPresent("kcm", record::kcm)
    }

private val columnList = listOf(id, jxlmc, jsmph, jasdm, skzws, zylxdm, jcKs, jcJs, day, sfyxzx, jyytms, kcm)

fun ProMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Pro, completer)

fun ProMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Pro, completer)

fun ProMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Pro, completer)

fun ProMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun ProMapper.update(completer: UpdateCompleter) =
    update(this::update, Pro, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: ProRecord) =
    apply {
        set(jxlmc).equalTo(record::jxlmc)
        set(jsmph).equalTo(record::jsmph)
        set(jasdm).equalTo(record::jasdm)
        set(skzws).equalTo(record::skzws)
        set(zylxdm).equalTo(record::zylxdm)
        set(jcKs).equalTo(record::jcKs)
        set(jcJs).equalTo(record::jcJs)
        set(day).equalTo(record::day)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jyytms).equalTo(record::jyytms)
        set(kcm).equalTo(record::kcm)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: ProRecord) =
    apply {
        set(jxlmc).equalToWhenPresent(record::jxlmc)
        set(jsmph).equalToWhenPresent(record::jsmph)
        set(jasdm).equalToWhenPresent(record::jasdm)
        set(skzws).equalToWhenPresent(record::skzws)
        set(zylxdm).equalToWhenPresent(record::zylxdm)
        set(jcKs).equalToWhenPresent(record::jcKs)
        set(jcJs).equalToWhenPresent(record::jcJs)
        set(day).equalToWhenPresent(record::day)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jyytms).equalToWhenPresent(record::jyytms)
        set(kcm).equalToWhenPresent(record::kcm)
    }

fun ProMapper.updateByPrimaryKey(record: ProRecord) =
    update {
        set(jxlmc).equalTo(record::jxlmc)
        set(jsmph).equalTo(record::jsmph)
        set(jasdm).equalTo(record::jasdm)
        set(skzws).equalTo(record::skzws)
        set(zylxdm).equalTo(record::zylxdm)
        set(jcKs).equalTo(record::jcKs)
        set(jcJs).equalTo(record::jcJs)
        set(day).equalTo(record::day)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jyytms).equalTo(record::jyytms)
        set(kcm).equalTo(record::kcm)
        where(id, isEqualTo(record::id))
    }

fun ProMapper.updateByPrimaryKeySelective(record: ProRecord) =
    update {
        set(jxlmc).equalToWhenPresent(record::jxlmc)
        set(jsmph).equalToWhenPresent(record::jsmph)
        set(jasdm).equalToWhenPresent(record::jasdm)
        set(skzws).equalToWhenPresent(record::skzws)
        set(zylxdm).equalToWhenPresent(record::zylxdm)
        set(jcKs).equalToWhenPresent(record::jcKs)
        set(jcJs).equalToWhenPresent(record::jcJs)
        set(day).equalToWhenPresent(record::day)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jyytms).equalToWhenPresent(record::jyytms)
        set(kcm).equalToWhenPresent(record::kcm)
        where(id, isEqualTo(record::id))
    }