@file:JvmName("MainKt")

package cn.repigeons.njnu.classroom

import cn.repigeons.commons.utils.SpringUtils
import org.mybatis.spring.annotation.MapperScan
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.cloud.openfeign.EnableFeignClients
import org.springframework.scheduling.annotation.EnableAsync
import org.springframework.scheduling.annotation.EnableScheduling

@SpringBootApplication(scanBasePackages = ["cn.repigeons.njnu.classroom"])
@MapperScan(value = ["cn.repigeons.njnu.classroom.mbg.mapper", "cn.repigeons.njnu.classroom.mbg.dao"])
@EnableFeignClients
@EnableScheduling
@EnableAsync
class CoreApplication

fun main(args: Array<String>) {
    SpringUtils.context = runApplication<CoreApplication>(*args)
}