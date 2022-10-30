@file:JvmName("MainKt")

package cn.repigeons.njnu.classroom

import cn.repigeons.njnu.classroom.component.SpringContextHolder
import org.mybatis.spring.annotation.MapperScan
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.scheduling.annotation.EnableAsync
import org.springframework.scheduling.annotation.EnableScheduling

@SpringBootApplication(scanBasePackages = ["cn.repigeons.njnu.classroom"])
@MapperScan("cn.repigeons.njnu.classroom.mbg.mapper")
@EnableScheduling
@EnableAsync
class SpiderApplication

fun main(args: Array<String>) {
    SpringContextHolder.context = runApplication<SpiderApplication>(*args)
}