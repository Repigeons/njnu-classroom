package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.mbg.mapper.*
import cn.repigeons.njnu.classroom.mbg.model.NoticeRecord
import cn.repigeons.njnu.classroom.service.NoticeService
import cn.repigeons.njnu.classroom.service.RedisService
import com.alibaba.fastjson.JSON
import com.alibaba.fastjson.JSONObject
import org.springframework.stereotype.Service
import java.text.SimpleDateFormat
import java.util.*

@Service
class NoticeServiceImpl(
    private val redisService: RedisService,
    private val noticeMapper: NoticeMapper
) : NoticeService {
    private val df = SimpleDateFormat("yyyy-MM-dd")

    override fun getNotice(): JSONObject {
        return redisService["notice"]?.let {
            JSON.parseObject(it)
        } ?: let {
            val record = noticeMapper.select {
                orderBy(NoticeDynamicSqlSupport.Notice.time.descending())
                limit(1)
            }.firstOrNull()
            val data = record2data(record)
            record?.run {
                redisService["notice"] = data.toJSONString()
            }
            data
        }
    }

    override fun setNotice(id: Int): JSONObject {
        val record = noticeMapper.selectByPrimaryKey(id)
        val data = record2data(record)
        record?.run {
            redisService["notice"] = data.toJSONString()
            return data
        }
        return getNotice()
    }

    override fun addNotice(text: String): JSONObject {
        val record = NoticeRecord(
            time = Date(),
            text = text
        )
        noticeMapper.insert(record)
        val data = record2data(record)
        redisService["notice"] = data.toJSONString()
        return data
    }

    private fun record2data(record: NoticeRecord?) = record?.let {
        val timestamp = it.time!!.time / 1000
        val date = df.format(it.time)
        JSONObject().apply {
            put("id", it.id)
            put("timestamp", timestamp)
            put("date", date)
            put("text", it.text)
        }
    } ?: JSONObject()
}