package cn.repigeons.njnu.classroom

import org.mybatis.spring.annotation.MapperScan
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.context.ApplicationContext
import org.springframework.scheduling.annotation.EnableAsync
import org.springframework.scheduling.annotation.EnableScheduling

@SpringBootApplication(scanBasePackages = ["cn.repigeons.njnu.classroom"])
@MapperScan("cn.repigeons.njnu.classroom.mbg.mapper")
@EnableScheduling
@EnableAsync
open class ExploreApplication

lateinit var context: ApplicationContext

fun main(args: Array<String>) {
    context = runApplication<ExploreApplication>(*args)
}