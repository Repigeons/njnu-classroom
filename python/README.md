# [NjnuClassroom 南师教室](../README.md)

## 第一部分 数据采集器

### 1、简介

该部分为“南师教室”项目的数据采集部分，主要用于从"南京师范大学一站式事务中心"爬取教室数据并存入数据库，应作为计划任务每日定时执行。
该部分采用基于Python的爬虫技术，获取一站式事务中心提供的数据，对数据进行统一化处理并存入数据库。

### 2、开发语言及环境

项目该部分采用JetBrains PyCharm集成开发环境进行开发，选用了Python编程语言，使用了`selenium`和`requests`爬虫框架和`PyMySQL`数据库操作包。

### 3、配置文件

在`conf`配置文件夹下，应包含`account.json`、`database.json`和`mail.json`三个配置文件，分别为爬取数据时使用的一站式账户、项目使用的数据库配置和运行时错误的邮件反馈，文件格式参考`template.*.json`模板文件

### 4、部署方法

Python语言具备良好的跨平台特性，可通过`virtualenv`模块快速建立项目虚拟环境。
具体命令如下：

```powershell
# Windows PowerShell
virtualenv env
./env/Script/activate
pip install -r requirements.txt
python Main.py
```

```bash
# Linux Bash / MacOS Terminal
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
python Main.py
```

### 5、项目结构

```Markdown
├── conf                    # 项目配置文件
│   ├── account.json        # 可用的一站式账户
│   ├── database.json       # 项目使用的数据库配置
│   ├── mail.json           # 项目使用的邮件配置
│   └── template.*.json     # 配置文件对应的模板
├── app                     # Python代码，核心过程
│   ├── __init__.py
│   ├── _core_data.py       # 获取详细课程数据
│   ├── _get_classrooms.py  # 获取教学楼及教室信息
│   ├── _get_cookies.py     # 获取cookies
│   └── _get_time.py        # 时间相关信息
├── utils                   # Python代码，工具函数
│   ├── __init__.py
│   ├── _mysql.py           # 数据库操作类
│   ├── _smtp.py            # 发件服务器操作类
│   ├── database_manager.py # 数据库业务模块
│   └── mail_manager.py     # 邮件业务模块
├── Main.py                 # 应用主入口
└── requirements.txt        # 项目所需的包和库
```

### 6、附录

#### 6.1 数据库

数据库中共包含5张数据表，分别为：

- 教室列表 `JAS`
- 原始课程表 `KCB`
- 校正表 `correction`
- 开发环境数据表 `dev`
- 生产环境数据表 `pro`

** 数据库创建语句可在 [`create.sql`](../create.sql) 文件中查询。

#### 6.2 项目中使用到的api地址

- 查询当前学年学期

> <http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxdqxnxq.do>

- 查询当前周次和总周次

> <http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do>

- 查询总教学周次

> <http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do>

- 获取全部教学楼教室信息

> <http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxjsxx.do>

- 获取指定教室指定周次的数据

> <http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do>

** 以上仅为简单枚举，具体用法(请求头及请求参数请参考源码及注释)
