/*
 * This file was generated by the Gradle 'init' task.
 */

plugins {
    `java-library`
    `maven-publish`
    `application`
}

repositories {
    maven("https://mirrors.repigeons.cn/repository/maven-public/")
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:2.7.5")
    implementation("cn.repigeons:spring-boot-commons:0.1.0-RELEASE")
}

application.mainClass.set("cn.repigeons.njnu.classroom.MainKt")
