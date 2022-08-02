package cn.repigeons.njnu.classroom.component

import org.springframework.context.ApplicationContext

object SpringContextHolder {
    lateinit var context: ApplicationContext
    inline fun <reified T> getBean(): T = T::class.java.getBean()
    fun <T> Class<T>.getBean(): T = context.getBean(this)
}