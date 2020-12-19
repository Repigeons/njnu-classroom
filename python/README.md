# [NjnuClassroom 南师教室](../README.md)

## 第一部分 数据服务器

### 1、简介

该部分为项目的后端数据服务，分为三个模块，分别用于从一站式事务中心获取数据并整理、提供详细数据服务以及发布公告信息。

### 2、开发语言及环境

该部分全部使用 Python 编程语言，采用 JetBrains PyCharm 集成开发环境进行开发，使用到的模块包括：

```text
certifi==2020.11.8
chardet==3.0.4
click==7.1.2
Flask==1.1.2
idna==2.10
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
PyMySQL==0.10.1
requests==2.25.0
selenium==3.141.0
urllib3==1.26.2
Werkzeug==1.0.1
```

### 3、配置文件

在 `conf` 配置文件夹下，包含 `account.json` `database.json` `mail.json` `selenium.json` 和 `spider.json` `server.json` `notice.json`，其中前四个为工具配置文件，后三个为服务模块配置文件，配置文件模版均在 `template.*.json`。

### 4、部署方法

Python语言具备良好的跨平台特性，可通过`virtualenv`模块快速建立项目虚拟环境。
具体命令如下：

```powershell
# Windows PowerShell
virtualenv env
./env/Script/activate
pip install -r requirements.txt
```

```bash
# Linux Bash
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
```

### 5、运行方法

该部分同时具备 `Script 启动` 和 `Module 启动` 两种方式，在激活虚拟环境后，可使用以下任意一种方式启动：

** 使用方式一或方式二可使用--conf参数设置配置文件目录，方式三许需要预设置`conf`环境变量

```shell
# 方式一：通过 manage 脚本启动服务模块
python manage.py --run Spider [--conf <config-directory:conf/>]
python manage.py --run Server [--conf <config-directory:conf/>]
python manage.py --run Notice [--conf <config-directory:conf/>]
```

```shell
# 方式二：通过 manage 模块启动服务模块
python -m manage --run Spider [--conf <config-directory:conf/>]
python -m manage --run Server [--conf <config-directory:conf/>]
python -m manage --run Notice [--conf <config-directory:conf/>]
```

```shell
# 方式三：直接启动服务模块
python -m App.Spider
python -m App.Server
python -m App.Notice
```

### 6、项目结构

```text
├── conf                    # 项目配置文件
│   ├── account.json        # 可用的一站式账户
│   ├── database.json       # 项目使用的数据库配置
│   ├── mail.json           # 项目使用的邮件服务器配置
│   ├── selenium.json       # selenium模拟浏览器配置
│   ├── spider.json         # 爬虫服务模块配置
│   ├── server.json         # 数据服务模块配置
│   ├── notice.json         # 公告服务模块配置
│   └── template.*.json     # 配置文件对应的模板
├── App                     # 应用模块
│   ├── public              # 公用工具模块
│   ├── Spider              # 爬虫服务模块
│   ├── Server              # 数据服务模块
│   └── Notice              # 公告服务模块
├── utils                   # 工具类
│   ├── __init__.py
│   ├── _mysql.py           # 数据库操作类
│   ├── _smtp.py            # 发件服务器操作类
│   └── _threading.py       # 多线程操作类
├── manage.py               # 模块主入口
└── requirements.txt        # 项目所需的包和库
```

### 6、附录

#### 6.1 数据库

数据库中共包含 6 张数据表：

- 教室列表 `JAS`
- 原始课程表 `KCB`
- 校正表 `correction`
- 开发环境数据表 `dev`
- 生产环境数据表 `pro`
- 用户反馈元数据 `feedback_metadata`

和 1 张数据视图：

- 用户反馈汇总信息 `feedback`

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

** 以上仅为简单枚举，具体用法（请求头及请求参数）请参考源码及注释
