/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-09T16:02:51.362+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.day
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.id
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.jcJs
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.jcKs
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.jsmph
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.jxlmc
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.jyytms
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.kcm
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.sfyxzx
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.skzws
import cn.repigeons.njnu.classroom.mbg.mapper.KcbDynamicSqlSupport.Kcb.zylxdm
import cn.repigeons.njnu.classroom.mbg.model.KcbRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun KcbMapper.count(completer: CountCompleter) =
    countFrom(this::count, Kcb, completer)

fun KcbMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Kcb, completer)

fun KcbMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun KcbMapper.insert(record: KcbRecord) =
    insert(this::insert, record, Kcb) {
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

fun KcbMapper.insertSelective(record: KcbRecord) =
    insert(this::insert, record, Kcb) {
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

fun KcbMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Kcb, completer)

fun KcbMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Kcb, completer)

fun KcbMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Kcb, completer)

fun KcbMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun KcbMapper.update(completer: UpdateCompleter) =
    update(this::update, Kcb, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: KcbRecord) =
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

fun KotlinUpdateBuilder.updateSelectiveColumns(record: KcbRecord) =
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

fun KcbMapper.updateByPrimaryKey(record: KcbRecord) =
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

fun KcbMapper.updateByPrimaryKeySelective(record: KcbRecord) =
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