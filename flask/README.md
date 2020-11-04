# [NjnuClassroom 南师教室](../README.md)

## 第二部分 数据服务器

### 1、简介

该部分为“南师教室”项目的服务端部分，主要用于提取并整理数据库中的数据，接受客户端发送的查询请求，根据请求内容返回相应数据。
该部分采用基于 Flask框架 的 api-service 开发模式，响应数据格式为`application/json`格式。

### 2、开发语言及环境

项目该部分采用JetBrains PyCharm集成开发环境进行开发，选用了Python编程语言，Flask框架。
Flask是一个使用Python编写的基于Werkzeug WSGI工具包的轻量级Web应用程序框架。

### 3、配置文件

在`conf`配置文件夹下，应包含`config.json`, `database.json`和`mail.json`三个配置文件，为项目使用的各项配置，文件格式参考`template.database.json`和`template.mail.json`模板文件。

### 4、部署方法

该Flask项目同样采用Python语言进行开发，部署方法与普通Python项目相同，[点此参考该项目爬虫部分](../python/README.md#4)。

### 5、项目结构

```Markdown
├── app                     # 项目主体
│   ├── __init__.py
│   ├── app.py              # 基础启动器
│   └── config.py           # 配置加载项目通用配置
├── conf                    # 项目配置文件夹
│   ├── config.json         # 基本运行配置
│   ├── database.json       # 项目使用的数据库配置
│   ├── mail.json           # 邮件服务器配置
│   └── template.*.json     # 配置文件对应的模板
├── handler                 # 请求处理器
│   ├── __init__.py
│   ├── Classroom.py        # Classroom类定义
│   ├── Empty.py            # 空教室查询
│   ├── Overview.py         # 教室概览
│   └── SearchMore.py       # 更多搜索
├── utils                   # 工具文件夹
│   ├── __init__.py
│   ├── _mysql.py           # 数据库操作类
│   ├── _stmp.py            # 邮件服务器类
│   ├── db_manager.py       # 应用数据库管理
│   └── mail_manager.py     # 应用邮件服务器
├── Main.py                 # 应用主入口
└── requirements.txt        # 项目所需的包和库
```
