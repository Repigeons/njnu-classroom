/*
 * Auto-generated file. Created by MyBatis Generator
 * Generation date: 2022-02-13T01:36:08.513+08:00
 */
package cn.repigeons.njnu.classroom.mbg.mapper

import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackMetadataDynamicSqlSupport.FeedbackMetadata
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackMetadataDynamicSqlSupport.FeedbackMetadata.id
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackMetadataDynamicSqlSupport.FeedbackMetadata.jasdm
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackMetadataDynamicSqlSupport.FeedbackMetadata.jc
import cn.repigeons.njnu.classroom.mbg.mapper.FeedbackMetadataDynamicSqlSupport.FeedbackMetadata.time
import cn.repigeons.njnu.classroom.mbg.model.FeedbackMetadataRecord
import org.mybatis.dynamic.sql.SqlBuilder.isEqualTo
import org.mybatis.dynamic.sql.util.kotlin.*
import org.mybatis.dynamic.sql.util.kotlin.mybatis3.*

fun FeedbackMetadataMapper.count(completer: CountCompleter) =
    countFrom(this::count, FeedbackMetadata, completer)

fun FeedbackMetadataMapper.delete(completer: DeleteCompleter) =
    deleteFrom(this::delete, FeedbackMetadata, completer)

fun FeedbackMetadataMapper.deleteByPrimaryKey(id_: Int) =
    delete {
        where(id, isEqualTo(id_))
    }

fun FeedbackMetadataMapper.insert(record: FeedbackMetadataRecord) =
    insert(this::insert, record, FeedbackMetadata) {
        map(time).toProperty("time")
        map(jc).toProperty("jc")
        map(jasdm).toProperty("jasdm")
    }

fun FeedbackMetadataMapper.insertSelective(record: FeedbackMetadataRecord) =
    insert(this::insert, record, FeedbackMetadata) {
        map(time).toPropertyWhenPresent("time", record::time)
        map(jc).toPropertyWhenPresent("jc", record::jc)
        map(jasdm).toPropertyWhenPresent("jasdm", record::jasdm)
    }

private val columnList = listOf(id, time, jc, jasdm)

fun FeedbackMetadataMapper.selectOne(completer: SelectCompleter) =
    selectOne(this::selectOne, columnList, FeedbackMetadata, completer)

fun FeedbackMetadataMapper.select(completer: SelectCompleter) =
    selectList(this::selectMany, columnList, FeedbackMetadata, completer)

fun FeedbackMetadataMapper.selectDistinct(completer: SelectCompleter) =
    selectDistinct(this::selectMany, columnList, FeedbackMetadata, completer)

fun FeedbackMetadataMapper.selectByPrimaryKey(id_: Int) =
    selectOne {
        where(id, isEqualTo(id_))
    }

fun FeedbackMetadataMapper.update(completer: UpdateCompleter) =
    update(this::update, FeedbackMetadata, completer)

fun KotlinUpdateBuilder.updateAllColumns(record: FeedbackMetadataRecord) =
    apply {
        set(time).equalTo(record::time)
        set(jc).equalTo(record::jc)
        set(jasdm).equalTo(record::jasdm)
    }

fun KotlinUpdateBuilder.updateSelectiveColumns(record: FeedbackMetadataRecord) =
    apply {
        set(time).equalToWhenPresent(record::time)
        set(jc).equalToWhenPresent(record::jc)
        set(jasdm).equalToWhenPresent(record::jasdm)
    }

fun FeedbackMetadataMapper.updateByPrimaryKey(record: FeedbackMetadataRecord) =
    update {
        set(time).equalTo(record::time)
        set(jc).equalTo(record::jc)
        set(jasdm).equalTo(record::jasdm)
        where(id, isEqualTo(record::id))
    }

fun FeedbackMetadataMapper.updateByPrimaryKeySelective(record: FeedbackMetadataRecord) =
    update {
        set(time).equalToWhenPresent(record::time)
        set(jc).equalToWhenPresent(record::jc)
        set(jasdm).equalToWhenPresent(record::jasdm)
        where(id, isEqualTo(record::id))
    }