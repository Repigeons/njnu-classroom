# 后端服务器 @[南师教室NjnuClassroom](../README.md)

## 1、简介

该部分为项目的后端数据服务，分为四个模块，分别为：

- spider：爬虫模块，从一站式事务中心获取数据并整理
- server：数据服务模块，向小程序提供教室信息服务
- explore: 发现服务模块，向小程序提供其他信息服务
- notice：公告服务模块，用于发布/回滚公告信息

## 2、服务器环境依赖

- Python3.9
- MariaDB
- Redis
- Nginx

## 3、开发语言及环境

该部分选用 `Python` 编程语言，使用 `VS Code` 与 `JetBrains PyCharm` 集成开发环境进行开发，使用到的模块包括：

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

## 4、资源文件

所有资源文件均放置在 `resources` 文件夹下， 其中 `application.yml` 为应用配置文件，包含数据库、邮件服务器在内的各项配置信息。

## 5、Docker部署（推荐）

该部分已被制作为 docker 镜像，位于 DockerHub 中。

镜像地址：docker.io/repigeons/njnu-classroom

运行所依赖的 python3.9 和 chromium 已被添加至镜像中。

docker容器 使用方式：

(1) 启动 mysql

```bash
# 拉取镜像
docker pull mariadb
# 第一次启动需要初始化root密码
docker run -itd \
  --name mysql-for-njnu-classroom \
  --volume /opt/docker/mysql:/var/lib/mysql \
  --env MYSQL_ROOT_PASSWORD=MyPassword \
  mariadb
# 连接数据库
docker exec -it mysql-for-njnu-classroom mysql -uroot -p
# 第二次直接启动即可
docker run -itd \
  --restart=always \
  --name mysql-for-njnu-classroom \
  --volume /opt/docker/mysql:/var/lib/mysql \
  mariadb
```

(2) 启动 redis

```bash
# 拉取镜像
docker pull redis
# 直接启动
docker run -itd \
  --restart=always \
  --name redis-for-njnu-classroom \
  redis
```

(3) 拉取南师教室的镜像

```bash
docker pull repigeons/njnu-classroom
```

(4) 建立数据卷（挂载卷）

```bash
# 建立挂载目录
mkdir /opt/docker/NjnuClassroom/resources
mkdir /opt/docker/NjnuClassroom/static
# 原始（模板）数据可以直接从git复制
```

(5) 启动容器

```bash
# 启动命令基本格式，各服务启动参数有差别
docker run -itd \
  --name njnu-classroom \
  --volume <宿主机文件目录>:<容器文件目录> \
  -p <宿主机端口>:<容器内端口> \
  -e env=<部署环境:dev/pro> \
  repigeons/njnu-classroom

# 启动 njnu-classroom-server
docker run -itd \
  --restart=always \
  --name njnu-classroom-server \
  --link mysql-for-njnu-classroom:mysql \
  --link redis-for-njnu-classroom:redis \
  --volume /opt/docker/NjnuClassroom:/data \
  -p 8001:80 \
  -e env=pro \
  repigeons/njnu-classroom \
  server

# 启动 njnu-classroom-explore
docker run -itd \
  --restart=always \
  --name njnu-classroom-explore \
  --link mysql-for-njnu-classroom:mysql \
  --link redis-for-njnu-classroom:redis \
  --volume /opt/docker/NjnuClassroom:/data \
  -p 8002:80 \
  repigeons/njnu-classroom \
  explore

# 启动 njnu-classroom-notice
docker run -itd \
  --restart=always \
  --name njnu-classroom-notice \
  --volume /opt/docker/NjnuClassroom:/data \
  -p 8010:80 \
  repigeons/njnu-classroom \
  notice

# 启动 njnu-classroom-spider
docker run --rm -d \
  --name njnu-classroom-spider \
  --link mysql-for-njnu-classroom:mysql \
  --link redis-for-njnu-classroom:redis \
  --volume /opt/docker/NjnuClassroom:/data \
  -e env=pro \
  repigeons/njnu-classroom \
  spider
```

## 6、其他部署方法

Python语言具备良好的跨平台特性，可通过`virtualenv`模块快速建立项目虚拟环境。 具体命令如下：

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt

# 在激活虚拟环境后，使用以下方式启动：
(env) python manage.py --run server  --log INFO
(env) python manage.py --run explore --log INFO
(env) python manage.py --run notice  --log INFO
(env) python manage.py --run spider  --log INFO
```

若需要直接运行项目，可使用 systemd 守护进程， service 文件示例位于 systemd 文件夹中。

## 7、项目结构

```text
server[NjnuClassroom]
├── resources               # 资源文件
│   ├── application.yml     # 应用配置文件
│   ├── stations.csv        # 校车站列表
│   └── notice.html         # 公告发布B端页面
├── shell                   # 启动脚本
├── static                  # 服务静态数据文件
├── systemd                 # Systemd守护配置文件
├── src                     # Python源码
│   ├── manage.py           # 模块唯一主入口
│   ├── app                 # 服务器模块
│   │   ├── app             # aiohttp模块
│   │   ├── RequestLoader   # HTTP请求预处理类
│   │   ├── JsonResponse    # HTTP响应格式化类
│   │   ├── PageResult      # 分页查询类
│   │   ├── mail            # smtp模块
│   │   ├── mysql           # mysql模块
│   │   └── redis           # redis模块
│   ├── modules             # 服务模块
│   │   ├── spider          # 爬虫模块
│   │   ├── server          # 数据服务模块
│   │   ├── explore         # 发现服务模块
│   │   └── notice          # 公告服务模块
│   └── orm                 # 对象关系映射
└── requirements.txt        # pip依赖包列表
```

## 8、附录

### 8.1 数据库

数据库中共包含 7 张数据表：

- 教室列表 `JAS`
- 原始课程表 `KCB`
- 校正表 `correction`
- 测试环境数据表 `dev`
- 生产环境数据表 `pro`
- 用户反馈元数据 `feedback_metadata`
- 校车时刻表 `shuttle`

和 1 张数据视图：

- 用户反馈汇总信息 `feedback`

** 数据库创建SQL位于
> [`create_main.sql`](../sql/create_main.sql) \
> [`create_explore.sql`](../sql/create_explore.sql)

### 8.2 项目中使用到的api地址

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
