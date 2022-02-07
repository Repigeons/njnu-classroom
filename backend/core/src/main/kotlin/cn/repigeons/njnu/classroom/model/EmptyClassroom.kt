package cn.repigeons.njnu.classroom.model

class EmptyClassroom {
    /**
     * 教室代码
     */
    lateinit var jasdm: String

    /**
     * 教室门牌号
     */
    lateinit var jsmph: String

    /**
     * 上课座位数
     */
    var skzws: Int = 0

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
}