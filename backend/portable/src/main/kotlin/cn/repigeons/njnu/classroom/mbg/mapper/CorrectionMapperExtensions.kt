/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-09T16:02:51.379+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.day
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.id
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.jcJs
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.jcKs
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.jsmph
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.jxlmc
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.jyytms
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.kcm
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.sfyxzx
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.skzws
import cn.repigeons.njnu.classroom.mbg.mapper.CorrectionDynamicSqlSupport.Correction.zylxdm
import cn.repigeons.njnu.classroom.mbg.model.CorrectionRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun CorrectionMapper.count(completer: CountCompleter) =
    countFrom(this::count, Correction, completer)

fun CorrectionMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Correction, completer)

fun CorrectionMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun CorrectionMapper.insert(record: CorrectionRecord) =
    insert(this::insert, record, Correction) {
        map(day).toProperty("day")
        map(jxlmc).toProperty("jxlmc")
        map(jsmph).toProperty("jsmph")
        map(jasdm).toProperty("jasdm")
        map(skzws).toProperty("skzws")
        map(zylxdm).toProperty("zylxdm")
        map(jcKs).toProperty("jcKs")
        map(jcJs).toProperty("jcJs")
        map(sfyxzx).toProperty("sfyxzx")
        map(jyytms).toProperty("jyytms")
        map(kcm).toProperty("kcm")
    }

fun CorrectionMapper.insertSelective(record: CorrectionRecord) =
    insert(this::insert, record, Correction) {
        map(day).toPropertyWhenPresent("day", record::day)
        map(jxlmc).toPropertyWhenPresent("jxlmc", record::jxlmc)
        map(jsmph).toPropertyWhenPresent("jsmph", record::jsmph)
        map(jasdm).toPropertyWhenPresent("jasdm", record::jasdm)
        map(skzws).toPropertyWhenPresent("skzws", record::skzws)
        map(zylxdm).toPropertyWhenPresent("zylxdm", record::zylxdm)
        map(jcKs).toPropertyWhenPresent("jcKs", record::jcKs)
        map(jcJs).toPropertyWhenPresent("jcJs", record::jcJs)
        map(sfyxzx).toPropertyWhenPresent("sfyxzx", record::sfyxzx)
        map(jyytms).toPropertyWhenPresent("jyytms", record::jyytms)
        map(kcm).toPropertyWhenPresent("kcm", record::kcm)
    }

private val columnList = listOf(id, day, jxlmc, jsmph, jasdm, skzws, zylxdm, jcKs, jcJs, sfyxzx, jyytms, kcm)

fun CorrectionMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Correction, completer)

fun CorrectionMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Correction, completer)

fun CorrectionMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Correction, completer)

fun CorrectionMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun CorrectionMapper.update(completer: UpdateCompleter) =
    update(this::update, Correction, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: CorrectionRecord) =
    apply {
        set(day).equalTo(record::day)
        set(jxlmc).equalTo(record::jxlmc)
        set(jsmph).equalTo(record::jsmph)
        set(jasdm).equalTo(record::jasdm)
        set(skzws).equalTo(record::skzws)
        set(zylxdm).equalTo(record::zylxdm)
        set(jcKs).equalTo(record::jcKs)
        set(jcJs).equalTo(record::jcJs)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jyytms).equalTo(record::jyytms)
        set(kcm).equalTo(record::kcm)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: CorrectionRecord) =
    apply {
        set(day).equalToWhenPresent(record::day)
        set(jxlmc).equalToWhenPresent(record::jxlmc)
        set(jsmph).equalToWhenPresent(record::jsmph)
        set(jasdm).equalToWhenPresent(record::jasdm)
        set(skzws).equalToWhenPresent(record::skzws)
        set(zylxdm).equalToWhenPresent(record::zylxdm)
        set(jcKs).equalToWhenPresent(record::jcKs)
        set(jcJs).equalToWhenPresent(record::jcJs)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jyytms).equalToWhenPresent(record::jyytms)
        set(kcm).equalToWhenPresent(record::kcm)
    }

fun CorrectionMapper.updateByPrimaryKey(record: CorrectionRecord) =
    update {
        set(day).equalTo(record::day)
        set(jxlmc).equalTo(record::jxlmc)
        set(jsmph).equalTo(record::jsmph)
        set(jasdm).equalTo(record::jasdm)
        set(skzws).equalTo(record::skzws)
        set(zylxdm).equalTo(record::zylxdm)
        set(jcKs).equalTo(record::jcKs)
        set(jcJs).equalTo(record::jcJs)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jyytms).equalTo(record::jyytms)
        set(kcm).equalTo(record::kcm)
        where(id, isEqualTo(record::id))
    }

fun CorrectionMapper.updateByPrimaryKeySelective(record: CorrectionRecord) =
    update {
        set(day).equalToWhenPresent(record::day)
        set(jxlmc).equalToWhenPresent(record::jxlmc)
        set(jsmph).equalToWhenPresent(record::jsmph)
        set(jasdm).equalToWhenPresent(record::jasdm)
        set(skzws).equalToWhenPresent(record::skzws)
        set(zylxdm).equalToWhenPresent(record::zylxdm)
        set(jcKs).equalToWhenPresent(record::jcKs)
        set(jcJs).equalToWhenPresent(record::jcJs)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jyytms).equalToWhenPresent(record::jyytms)
        set(kcm).equalToWhenPresent(record::kcm)
        where(id, isEqualTo(record::id))
    }