package cn.repigeons.njnu.classroom

import cn.repigeons.njnu.classroom.component.SpringContextHolder
import org.mybatis.spring.annotation.MapperScan
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.cloud.openfeign.EnableFeignClients
import org.springframework.scheduling.annotation.EnableAsync
import org.springframework.scheduling.annotation.EnableScheduling

@SpringBootApplication(scanBasePackages = ["cn.repigeons.njnu.classroom"])
@MapperScan("cn.repigeons.njnu.classroom.mbg.mapper")
@EnableFeignClients
@EnableScheduling
@EnableAsync
open class CoreApplication

fun main(args: Array<String>) {
    SpringContextHolder.context = runApplication<CoreApplication>(*args)
}