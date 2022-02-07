/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-09T16:02:51.367+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.day
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.id
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.jcJs
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.jcKs
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.jsmph
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.jxlmc
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.jyytms
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.kcm
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.sfyxzx
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.skzws
import cn.repigeons.njnu.classroom.mbg.mapper.DevDynamicSqlSupport.Dev.zylxdm
import cn.repigeons.njnu.classroom.mbg.model.DevRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun DevMapper.count(completer: CountCompleter) =
    countFrom(this::count, Dev, completer)

fun DevMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Dev, completer)

fun DevMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun DevMapper.insert(record: DevRecord) =
    insert(this::insert, record, Dev) {
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

fun DevMapper.insertSelective(record: DevRecord) =
    insert(this::insert, record, Dev) {
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

fun DevMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Dev, completer)

fun DevMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Dev, completer)

fun DevMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Dev, completer)

fun DevMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun DevMapper.update(completer: UpdateCompleter) =
    update(this::update, Dev, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: DevRecord) =
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

fun KotlinUpdateBuilder.updateSelectiveColumns(record: DevRecord) =
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

fun DevMapper.updateByPrimaryKey(record: DevRecord) =
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

fun DevMapper.updateByPrimaryKeySelective(record: DevRecord) =
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