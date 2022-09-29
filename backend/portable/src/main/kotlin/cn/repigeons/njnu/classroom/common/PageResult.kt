package cn.repigeons.njnu.classroom.common

import com.github.pagehelper.PageInfo


class PageResult<T>() {
    var page: Int = 0
    var size: Int = 0
    var pageCount: Int = 0
    var totalCount: Long = 0
    lateinit var list: List<T>

    constructor(list: List<T>) : this() {
        val pageInfo = PageInfo(list)
        this.page = pageInfo.pageNum
        this.size = pageInfo.pageSize
        this.pageCount = pageInfo.pages
        this.totalCount = pageInfo.total
        this.list = pageInfo.list
    }

    constructor(list: List<T>, pageInfo: PageInfo<*>) : this() {
        this.page = pageInfo.pageNum
        this.size = pageInfo.pageSize
        this.pageCount = pageInfo.pages
        this.totalCount = pageInfo.total
        this.list = list
    }

    companion object {
        fun <T> List<T>.pageInfo() = PageInfo(this)
    }
}