# [NjnuClassroom 南师教室](../README.md)

## 第一部分 数据服务器

### 1、简介

该部分为项目的后端数据服务，分为三个模块，分别为：

- Spider：从一站式事务中心获取数据并整理
- Server：向小程序提供数据服务
- Notice：发布公告信息

### 2、环境依赖

- python3
- redis
- nginx
- mariadb-server

### 3、开发语言及环境

该部分全部使用Python编程语言，采用 JetBrains PyCharm 集成开发环境进行开发，使用到的模块包括：

```text
certifi==2020.12.5
chardet==4.0.0
click==7.1.2
Flask==1.1.2
idna==2.10
itsdangerous==1.1.0
Jinja2==2.11.2
mariadb==1.0.5
MarkupSafe==1.1.1
python-redis-lock==3.7.0
PyYAML==5.3.1
redis==3.5.3
requests==2.25.1
selenium==3.141.0
urllib3==1.26.2
Werkzeug==1.0.1
```

### 4、资源文件

所有资源文件均放置在 `resources` 文件夹下，
其中 `application.yml` 为应用配置文件，包含数据库、邮件服务器在内的各项配置信息。

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

Python语言具备良好的跨平台特性，可通过`virtualenv`模块快速建立项目虚拟环境。
具体命令如下：

```powershell
# Windows PowerShell
virtualenv env
./env/Script/activate
# cd ZTxLib
python -m setup install  # install ZTxLib
pip install -r requirements.txt
```

```bash
# Linux Bash
virtualenv env
source env/bin/activate
# cd ZTxLib
python -m setup install  # install ZTxLib
pip install -r requirements.txt
```

### 7、运行方法

该部分同时具备 `Script启动` 和 `Module启动` 两种方式，在激活虚拟环境后，可使用以下任意一种方式启动：

```shell
# 方式一：通过 manage 脚本启动服务模块
python manage.py -r Spider [-l <logging file>]
python manage.py -r Server [-l <logging file>]
python manage.py -r Notice [-l <logging file>]
```

```shell
# 方式二：通过 manage 模块启动服务模块
python -m manage --run Spider [--log <logging file>]
python -m manage --run Server [--log <logging file>]
python -m manage --run Notice [--log <logging file>]
```

### 8、systemd 守护进程

若直接运行项目，可使用 systemd 守护进程，
service 文件示例位于 systemd 文件夹中。

### 9、项目结构

```text
python(NjnuClassroom)
├── manage.py               # 模块主入口
├── App                     # 应用模块
│   ├── _public             # 公共模块
│   ├── Spider              # 爬虫服务模块
│   ├── Server              # 数据服务模块
│   └── Notice              # 公告服务模块
├── resources               # 资源文件
│   ├── ZTxLib              # submodule
│   └── application.yml     # 应用配置文件
└── requirements.txt        # pip依赖包列表
```

### 10、附录

#### 10.1 数据库

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
