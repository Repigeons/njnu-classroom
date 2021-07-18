# [NjnuClassroom 南师教室](../README.md)

## 第一部分 数据服务器

### 1、简介

该部分为项目的后端数据服务，分为四个模块，分别为：

- spider：爬虫模块，从一站式事务中心获取数据并整理
- server：数据服务模块，向小程序提供教室信息服务
- explore: 发现服务模块，向小程序提供其他信息服务
- notice：公告服务模块，用于发布公告信息

### 2、环境依赖

- python3
- Redis
- nginx
- mariadb-server

### 3、开发语言及环境

该部分全部使用Python编程语言，采用 JetBrains PyCharm 集成开发环境进行开发，使用到的模块包括：

```text
aiofiles==0.7.0
aiohttp==3.7.4.post0
aiomysql==0.0.21
aioredis==1.3.1
aiosmtplib==1.1.6
async-timeout==3.0.1
attrs==21.2.0
chardet==4.0.0
hiredis==2.0.0
idna==3.2
multidict==5.1.0
PyMySQL==0.9.3
PyYAML==5.4.1
selenium==3.141.0
typing-extensions==3.10.0.0
urllib3==1.26.6
yarl==1.6.3
```

### 4、资源文件

所有资源文件均放置在 `resources` 文件夹下， 其中 `application.yml` 为应用配置文件，包含数据库、邮件服务器在内的各项配置信息。

### 5、Docker部署（推荐）

该部分已被制作为 docker 镜像，位于 DockerHub 中。

镜像地址：docker.io/repigeons/njnu-classroom

运行所依赖的 python3, redis, nginx 和 chromium 已被添加至镜像中，宿主机中仅需安装 mariadb-server 并设置相应权限即可。

docker容器 使用方式：

```shell
# 拉取镜像
docker pull repigeons/njnu-classroom

# 使用该镜像创建容器
docker run --name <容器名称> -p <宿主机项目端口>:<容器开放端口> -v <宿主机中日志文件目录>:<容器中日志文件目录> -it repigeons/njnu-classroom
# 示例：
docker run --name njnu-classroom -p 8000:80 -v /var/log/NjnuClassroom:/var/log/NjnuClassroom -it repigeons/njnu-classroom
```

### 6、其他部署方法

Python语言具备良好的跨平台特性，可通过`virtualenv`模块快速建立项目虚拟环境。 具体命令如下：

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### 7、运行方法

在激活虚拟环境后，使用以下方式启动：

```shell
python -m manage --run spider  --log <log level(INFO)>
python -m manage --run server  --log <log level(INFO)>
python -m manage --run explore --log <log level(INFO)>
python -m manage --run notice  --log <log level(INFO)>
```

### 8、systemd 守护进程

若直接运行项目，可使用 systemd 守护进程， service 文件示例位于 systemd 文件夹中。

### 9、项目结构

```text
python(NjnuClassroom)
├── manage.py               # 模块主入口
├── app                     # 服务器模块
│   ├── app                 # aiohttp模块
│   ├── mail                # smtp模块
│   ├── mysql               # mysql模块
│   └── redis               # redis模块
├── modules                 # 服务模块
│   ├── spider              # 爬虫模块
│   ├── server              # 数据服务模块
│   ├── explore             # 发现服务模块
│   └── notice              # 公告服务模块
├── orm                     # 对象关系映射
├── resources               # 资源文件
│   ├── application.yml     # 应用配置文件
│   └── stations.csv        # 校车站列表
└── requirements.txt        # pip依赖包列表
```

### 10、附录

#### 10.1 数据库

数据库中共包含 7 张数据表：

- 教室列表 `JAS`
- 原始课程表 `KCB`
- 校正表 `correction`
- 开发环境数据表 `dev`
- 生产环境数据表 `pro`
- 用户反馈元数据 `feedback_metadata`
- 校车时刻表 `shuttle`

和 1 张数据视图：

- 用户反馈汇总信息 `feedback`

** 数据库创建语句可在 [`create_main.sql`](../create_main.sql) 文件中查询。

#### 10.2 项目中使用到的api地址

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
