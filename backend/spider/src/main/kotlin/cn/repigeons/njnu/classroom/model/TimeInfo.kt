package cn.repigeons.njnu.classroom.model

class TimeInfo {
    /**
     * 学年学期代码
     */
    lateinit var XNXQDM: String

    /**
     * 学年代码
     */
    lateinit var XNDM: String

    /**
     * 学期代码
     */
    lateinit var XQDM: String

    /**
     * 周次
     */
    var ZC: Int = 0

    /**
     * 总周次
     */
    var ZZC: Int = 0

    /**
     * 总教学周次
     */
    var ZJXZC: Int = 0

    override fun toString(): String {
        return mapOf(
            *javaClass.fields.map {
                Pair(it.name, it.get(this))
            }.toTypedArray()
        ).toString()
    }
}