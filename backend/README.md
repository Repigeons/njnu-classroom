# 后端微服务 @[南师教室NjnuClassroom](../README.md)

## 1、简介

该部分为项目的后端微服务，主要用于各类数据的采集整理存储与查询。
该部分采用maven构建，使用了基于SpringBoot的微服务架构。

## 2、开发语言及环境

该部分选用 `Kotlin` 编程语言，使用 `JetBrains IntelliJ IDEA` 进行开发。
Kotlin 是由JetBrains开发的运行于JVM的静态类型编程语言。

## 3、构建方法

该部分采用 maven 构建，运行于 Docker 环境，使用 docker-compose 进行容器编排。
各模块所使用的Dockerfile与compose文件位于dockerfile目录下。
完整的部署流程均已实现自动化，编写与Makefile中，在Linux操作系统下可直接使用。

## 4、项目结构

```text
├── Makefile                # 自动化部署脚本
├── pom.xml                 # 全局maven配置
├── dockerfile              # Dockerfile与compose文件
├── portable/               # 通用工具模块
│   ├── src
│   └── pom.xml             # 模块maven配置
├── spider/                 # 爬虫微服务模块
│   ├── src
│   └── pom.xml             # 模块maven配置
├── core/                   # 教室数据微服务模块
│   ├── src
│   └── pom.xml             # 模块maven配置
└── explore/                # 发现区微服务模块
    ├── src
    └── pom.xml             # 模块maven配置
```
