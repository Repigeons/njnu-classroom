/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-11-24T19:04:19.957+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.bz
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.dwdm
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.dwdmDisplay
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.jaslxdm
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.jaslxdmDisplay
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.jasmc
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.jsyt
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.jxldm
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.jxldmDisplay
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.ksyxj
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.kszws
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.lc
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.pkyxj
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sfkswh
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sfypk
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sfyxcx
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sfyxjy
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sfyxks
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sfyxpk
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sfyxzx
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.skzws
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sxlb
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.syrq
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.sysj
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.xgdd
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.xnxqdm
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.xnxqdm2
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.xxxqdm
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.xxxqdmDisplay
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.zt
import cn.repigeons.njnu.classroom.mbg.mapper.JasDynamicSqlSupport.Jas.zwsxdm
import cn.repigeons.njnu.classroom.mbg.model.JasRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun JasMapper.count(completer: CountCompleter) =
    countFrom(this::count, Jas, completer)

fun JasMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, Jas, completer)

fun JasMapper.deleteByPrimaryKey(jasdm_: String) =
    delete {
        where(jasdm, isEqualTo(jasdm_))
    }

fun JasMapper.insert(record: JasRecord) =
    insert(this::insert, record, Jas) {
        map(jasmc).toProperty("jasmc")
        map(jxldm).toProperty("jxldm")
        map(jxldmDisplay).toProperty("jxldmDisplay")
        map(xxxqdm).toProperty("xxxqdm")
        map(xxxqdmDisplay).toProperty("xxxqdmDisplay")
        map(jaslxdm).toProperty("jaslxdm")
        map(jaslxdmDisplay).toProperty("jaslxdmDisplay")
        map(zt).toProperty("zt")
        map(lc).toProperty("lc")
        map(skzws).toProperty("skzws")
        map(kszws).toProperty("kszws")
        map(xnxqdm).toProperty("xnxqdm")
        map(xnxqdm2).toProperty("xnxqdm2")
        map(dwdm).toProperty("dwdm")
        map(dwdmDisplay).toProperty("dwdmDisplay")
        map(zwsxdm).toProperty("zwsxdm")
        map(syrq).toProperty("syrq")
        map(sysj).toProperty("sysj")
        map(sxlb).toProperty("sxlb")
        map(sfypk).toProperty("sfypk")
        map(sfyxpk).toProperty("sfyxpk")
        map(pkyxj).toProperty("pkyxj")
        map(sfkswh).toProperty("sfkswh")
        map(sfyxks).toProperty("sfyxks")
        map(ksyxj).toProperty("ksyxj")
        map(sfyxcx).toProperty("sfyxcx")
        map(sfyxjy).toProperty("sfyxjy")
        map(sfyxzx).toProperty("sfyxzx")
        map(jsyt).toProperty("jsyt")
        map(xgdd).toProperty("xgdd")
        map(bz).toProperty("bz")
    }

fun JasMapper.insertSelective(record: JasRecord) =
    insert(this::insert, record, Jas) {
        map(jasmc).toPropertyWhenPresent("jasmc", record::jasmc)
        map(jxldm).toPropertyWhenPresent("jxldm", record::jxldm)
        map(jxldmDisplay).toPropertyWhenPresent("jxldmDisplay", record::jxldmDisplay)
        map(xxxqdm).toPropertyWhenPresent("xxxqdm", record::xxxqdm)
        map(xxxqdmDisplay).toPropertyWhenPresent("xxxqdmDisplay", record::xxxqdmDisplay)
        map(jaslxdm).toPropertyWhenPresent("jaslxdm", record::jaslxdm)
        map(jaslxdmDisplay).toPropertyWhenPresent("jaslxdmDisplay", record::jaslxdmDisplay)
        map(zt).toPropertyWhenPresent("zt", record::zt)
        map(lc).toPropertyWhenPresent("lc", record::lc)
        map(skzws).toPropertyWhenPresent("skzws", record::skzws)
        map(kszws).toPropertyWhenPresent("kszws", record::kszws)
        map(xnxqdm).toPropertyWhenPresent("xnxqdm", record::xnxqdm)
        map(xnxqdm2).toPropertyWhenPresent("xnxqdm2", record::xnxqdm2)
        map(dwdm).toPropertyWhenPresent("dwdm", record::dwdm)
        map(dwdmDisplay).toPropertyWhenPresent("dwdmDisplay", record::dwdmDisplay)
        map(zwsxdm).toPropertyWhenPresent("zwsxdm", record::zwsxdm)
        map(syrq).toPropertyWhenPresent("syrq", record::syrq)
        map(sysj).toPropertyWhenPresent("sysj", record::sysj)
        map(sxlb).toPropertyWhenPresent("sxlb", record::sxlb)
        map(sfypk).toPropertyWhenPresent("sfypk", record::sfypk)
        map(sfyxpk).toPropertyWhenPresent("sfyxpk", record::sfyxpk)
        map(pkyxj).toPropertyWhenPresent("pkyxj", record::pkyxj)
        map(sfkswh).toPropertyWhenPresent("sfkswh", record::sfkswh)
        map(sfyxks).toPropertyWhenPresent("sfyxks", record::sfyxks)
        map(ksyxj).toPropertyWhenPresent("ksyxj", record::ksyxj)
        map(sfyxcx).toPropertyWhenPresent("sfyxcx", record::sfyxcx)
        map(sfyxjy).toPropertyWhenPresent("sfyxjy", record::sfyxjy)
        map(sfyxzx).toPropertyWhenPresent("sfyxzx", record::sfyxzx)
        map(jsyt).toPropertyWhenPresent("jsyt", record::jsyt)
        map(xgdd).toPropertyWhenPresent("xgdd", record::xgdd)
        map(bz).toPropertyWhenPresent("bz", record::bz)
    }

private val columnList = listOf(jasdm, jasmc, jxldm, jxldmDisplay, xxxqdm, xxxqdmDisplay, jaslxdm, jaslxdmDisplay, zt, lc, skzws, kszws, xnxqdm, xnxqdm2, dwdm, dwdmDisplay, zwsxdm, syrq, sysj, sxlb, sfypk, sfyxpk, pkyxj, sfkswh, sfyxks, ksyxj, sfyxcx, sfyxjy, sfyxzx, jsyt, xgdd, bz)

fun JasMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, Jas, completer)

fun JasMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, Jas, completer)

fun JasMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, Jas, completer)

fun JasMapper.selectByPrimaryKey(jasdm_: String) =
    selectOne {
        where(jasdm, isEqualTo(jasdm_))
    }

fun JasMapper.update(completer: UpdateCompleter) =
    update(this::update, Jas, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: JasRecord) =
    apply {
        set(jasmc).equalTo(record::jasmc)
        set(jxldm).equalTo(record::jxldm)
        set(jxldmDisplay).equalTo(record::jxldmDisplay)
        set(xxxqdm).equalTo(record::xxxqdm)
        set(xxxqdmDisplay).equalTo(record::xxxqdmDisplay)
        set(jaslxdm).equalTo(record::jaslxdm)
        set(jaslxdmDisplay).equalTo(record::jaslxdmDisplay)
        set(zt).equalTo(record::zt)
        set(lc).equalTo(record::lc)
        set(skzws).equalTo(record::skzws)
        set(kszws).equalTo(record::kszws)
        set(xnxqdm).equalTo(record::xnxqdm)
        set(xnxqdm2).equalTo(record::xnxqdm2)
        set(dwdm).equalTo(record::dwdm)
        set(dwdmDisplay).equalTo(record::dwdmDisplay)
        set(zwsxdm).equalTo(record::zwsxdm)
        set(syrq).equalTo(record::syrq)
        set(sysj).equalTo(record::sysj)
        set(sxlb).equalTo(record::sxlb)
        set(sfypk).equalTo(record::sfypk)
        set(sfyxpk).equalTo(record::sfyxpk)
        set(pkyxj).equalTo(record::pkyxj)
        set(sfkswh).equalTo(record::sfkswh)
        set(sfyxks).equalTo(record::sfyxks)
        set(ksyxj).equalTo(record::ksyxj)
        set(sfyxcx).equalTo(record::sfyxcx)
        set(sfyxjy).equalTo(record::sfyxjy)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jsyt).equalTo(record::jsyt)
        set(xgdd).equalTo(record::xgdd)
        set(bz).equalTo(record::bz)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: JasRecord) =
    apply {
        set(jasmc).equalToWhenPresent(record::jasmc)
        set(jxldm).equalToWhenPresent(record::jxldm)
        set(jxldmDisplay).equalToWhenPresent(record::jxldmDisplay)
        set(xxxqdm).equalToWhenPresent(record::xxxqdm)
        set(xxxqdmDisplay).equalToWhenPresent(record::xxxqdmDisplay)
        set(jaslxdm).equalToWhenPresent(record::jaslxdm)
        set(jaslxdmDisplay).equalToWhenPresent(record::jaslxdmDisplay)
        set(zt).equalToWhenPresent(record::zt)
        set(lc).equalToWhenPresent(record::lc)
        set(skzws).equalToWhenPresent(record::skzws)
        set(kszws).equalToWhenPresent(record::kszws)
        set(xnxqdm).equalToWhenPresent(record::xnxqdm)
        set(xnxqdm2).equalToWhenPresent(record::xnxqdm2)
        set(dwdm).equalToWhenPresent(record::dwdm)
        set(dwdmDisplay).equalToWhenPresent(record::dwdmDisplay)
        set(zwsxdm).equalToWhenPresent(record::zwsxdm)
        set(syrq).equalToWhenPresent(record::syrq)
        set(sysj).equalToWhenPresent(record::sysj)
        set(sxlb).equalToWhenPresent(record::sxlb)
        set(sfypk).equalToWhenPresent(record::sfypk)
        set(sfyxpk).equalToWhenPresent(record::sfyxpk)
        set(pkyxj).equalToWhenPresent(record::pkyxj)
        set(sfkswh).equalToWhenPresent(record::sfkswh)
        set(sfyxks).equalToWhenPresent(record::sfyxks)
        set(ksyxj).equalToWhenPresent(record::ksyxj)
        set(sfyxcx).equalToWhenPresent(record::sfyxcx)
        set(sfyxjy).equalToWhenPresent(record::sfyxjy)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jsyt).equalToWhenPresent(record::jsyt)
        set(xgdd).equalToWhenPresent(record::xgdd)
        set(bz).equalToWhenPresent(record::bz)
    }

fun JasMapper.updateByPrimaryKey(record: JasRecord) =
    update {
        set(jasmc).equalTo(record::jasmc)
        set(jxldm).equalTo(record::jxldm)
        set(jxldmDisplay).equalTo(record::jxldmDisplay)
        set(xxxqdm).equalTo(record::xxxqdm)
        set(xxxqdmDisplay).equalTo(record::xxxqdmDisplay)
        set(jaslxdm).equalTo(record::jaslxdm)
        set(jaslxdmDisplay).equalTo(record::jaslxdmDisplay)
        set(zt).equalTo(record::zt)
        set(lc).equalTo(record::lc)
        set(skzws).equalTo(record::skzws)
        set(kszws).equalTo(record::kszws)
        set(xnxqdm).equalTo(record::xnxqdm)
        set(xnxqdm2).equalTo(record::xnxqdm2)
        set(dwdm).equalTo(record::dwdm)
        set(dwdmDisplay).equalTo(record::dwdmDisplay)
        set(zwsxdm).equalTo(record::zwsxdm)
        set(syrq).equalTo(record::syrq)
        set(sysj).equalTo(record::sysj)
        set(sxlb).equalTo(record::sxlb)
        set(sfypk).equalTo(record::sfypk)
        set(sfyxpk).equalTo(record::sfyxpk)
        set(pkyxj).equalTo(record::pkyxj)
        set(sfkswh).equalTo(record::sfkswh)
        set(sfyxks).equalTo(record::sfyxks)
        set(ksyxj).equalTo(record::ksyxj)
        set(sfyxcx).equalTo(record::sfyxcx)
        set(sfyxjy).equalTo(record::sfyxjy)
        set(sfyxzx).equalTo(record::sfyxzx)
        set(jsyt).equalTo(record::jsyt)
        set(xgdd).equalTo(record::xgdd)
        set(bz).equalTo(record::bz)
        where(jasdm, isEqualTo(record::jasdm))
    }

fun JasMapper.updateByPrimaryKeySelective(record: JasRecord) =
    update {
        set(jasmc).equalToWhenPresent(record::jasmc)
        set(jxldm).equalToWhenPresent(record::jxldm)
        set(jxldmDisplay).equalToWhenPresent(record::jxldmDisplay)
        set(xxxqdm).equalToWhenPresent(record::xxxqdm)
        set(xxxqdmDisplay).equalToWhenPresent(record::xxxqdmDisplay)
        set(jaslxdm).equalToWhenPresent(record::jaslxdm)
        set(jaslxdmDisplay).equalToWhenPresent(record::jaslxdmDisplay)
        set(zt).equalToWhenPresent(record::zt)
        set(lc).equalToWhenPresent(record::lc)
        set(skzws).equalToWhenPresent(record::skzws)
        set(kszws).equalToWhenPresent(record::kszws)
        set(xnxqdm).equalToWhenPresent(record::xnxqdm)
        set(xnxqdm2).equalToWhenPresent(record::xnxqdm2)
        set(dwdm).equalToWhenPresent(record::dwdm)
        set(dwdmDisplay).equalToWhenPresent(record::dwdmDisplay)
        set(zwsxdm).equalToWhenPresent(record::zwsxdm)
        set(syrq).equalToWhenPresent(record::syrq)
        set(sysj).equalToWhenPresent(record::sysj)
        set(sxlb).equalToWhenPresent(record::sxlb)
        set(sfypk).equalToWhenPresent(record::sfypk)
        set(sfyxpk).equalToWhenPresent(record::sfyxpk)
        set(pkyxj).equalToWhenPresent(record::pkyxj)
        set(sfkswh).equalToWhenPresent(record::sfkswh)
        set(sfyxks).equalToWhenPresent(record::sfyxks)
        set(ksyxj).equalToWhenPresent(record::ksyxj)
        set(sfyxcx).equalToWhenPresent(record::sfyxcx)
        set(sfyxjy).equalToWhenPresent(record::sfyxjy)
        set(sfyxzx).equalToWhenPresent(record::sfyxzx)
        set(jsyt).equalToWhenPresent(record::jsyt)
        set(xgdd).equalToWhenPresent(record::xgdd)
        set(bz).equalToWhenPresent(record::bz)
        where(jasdm, isEqualTo(record::jasdm))
    }