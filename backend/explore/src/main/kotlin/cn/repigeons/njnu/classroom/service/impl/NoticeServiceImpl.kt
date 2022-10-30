package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.NoticeRecord
import cn.repigeons.njnu.classroom.service.NoticeService
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.util.GsonUtil
import org.springframework.stereotype.Service
import java.text.SimpleDateFormat
import java.util.*

@Service
class NoticeServiceImpl(
    private val redisService: RedisService,
    private val noticeMapper: NoticeMapper
) : NoticeService {
    private val df = SimpleDateFormat("yyyy-MM-dd")

    override fun get(): Map<*, *> {
        return redisService["notice"]?.let {
            GsonUtil.fromJson(it)
        } ?: let {
            val record = noticeMapper.select {
                orderBy(NoticeDynamicSqlSupport.Notice.time.descending())
                limit(1)
            }.firstOrNull()
            val data = record2data(record)
            record?.run {
                redisService["notice"] = GsonUtil.toJson(data)
            }
            data
        }
    }

    override fun set(id: Int): Map<*, *> {
        val record = noticeMapper.selectByPrimaryKey(id)
        val data = record2data(record)
        record?.run {
            redisService["notice"] = GsonUtil.toJson(data)
            return data
        }
        return get()
    }

    override fun add(text: String): Map<*, *> {
        val record = NoticeRecord(
            time = Date(),
            text = text
        )
        noticeMapper.insert(record)
        val data = record2data(record)
        redisService["notice"] = GsonUtil.toJson(data)
        return data
    }

    private fun record2data(record: NoticeRecord?) = record?.let {
        val timestamp = record.time!!.time / 1000
        val date = df.format(record.time)
        mapOf(
            Pair("id", record.id),
            Pair("timestamp", timestamp),
            Pair("date", date),
            Pair("text", record.text)
        )
    } ?: mapOf()
}