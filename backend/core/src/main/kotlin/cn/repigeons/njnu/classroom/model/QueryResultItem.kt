package cn.repigeons.njnu.classroom.model

import cn.repigeons.njnu.classroom.mbg.model.TimetableRecord

class QueryResultItem() {
    constructor(record: TimetableRecord) : this() {
        this.jxlmc = record.jxlmc!!
        this.jsmph = record.jsmph!!
        this.skzws = record.skzws!!
        this.day = record.weekday!!
        this.jcKs = record.jcKs!!
        this.jcJs = record.jcJs!!
        this.zylxdm = record.zylxdm!!
        this.jyytms = record.jyytms!!
        this.kcm = record.kcm!!
    }

    /**
     * 教学楼名称
     */
    lateinit var jxlmc: String

    /**
     * 教室门牌号
     */
    lateinit var jsmph: String

    /**
     * 上课座位数
     */
    var skzws: Int = 0

    /**
     * 星期
     */
    lateinit var day: String

    /**
     * 开始节次
     */
    var jcKs: Short = 0

    /**
     * 结束节次
     */
    var jcJs: Short = 0

    /**
     * 资源类型代码
     */
    lateinit var zylxdm: String

    /**
     * 借用用途说明
     */
    lateinit var jyytms: String

    /**
     * 课程名
     */
    lateinit var kcm: String
}