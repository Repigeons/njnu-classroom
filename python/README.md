# [NjnuClassroom 南师教室](../README.md)
## 第一部分 数据采集器


### 1、简介
该部分为“南师教室”项目的数据采集部分，主要用于从"南京师范大学一站式事务中心"爬取教室数据并存入数据库，应作为计划任务每日定时执行。
该部分采用基于Python的爬虫技术，获取一站式事务中心提供的数据，对数据进行统一化处理并存入数据库。


### 2、开发语言及环境
项目该部分采用JetBrains PyCharm集成开发环境进行开发，选用了Python编程语言，使用了`selenium`和`requests`爬虫框架和`PyMySQL`数据库操作包。


### 3、配置文件
在`conf`配置文件夹下，应包含`account.json`与`database.json`两个配置文件，分别为爬取数据时使用的一站式账户和项目使用的数据库配置，文件格式参考`template.*.json`模板文件


### 4、部署方法
Python语言具备良好的跨平台特性，可通过`virtualenv`模块快速建立项目虚拟环境。
具体命令如下：
```
# Windows cmd
python -m venv ENV
ENV\Script\activate.bat
pip install -r requirements.txt
python Main.py

# Windows powershell
python -m venv ENV
./ENV/Script/Activate.ps1
pip install -r requirements.txt
python Main.py

# Linux bash
python3 -m venv ENV
source ./ENV/bin/activate
pip install -r requirements.txt
python Main.py

# MacOS Terminal
python3 -m venv ENV
source ./ENV/bin/activate
pip install -r requirements.txt
python Main.py
```


### 5、编译方法
除了利用Python解释性运行的方法，也可以先对项目进行编译，编译方法如下：

(1)安装PyInstaller，命令为
> pip3 install pyinstaller

(2)激活虚拟环境（参考[#4](#4部署方法)）
> (略)

(3)编译项目，命令为
> pyinstaller -F Main.py -p ENV/Lib/site-packages

（其中site-packages为虚拟环境目录下的该项目所引用的包，需根据具体情况填写该参数）


### 6、项目结构
```
├── requirements.txt        # 项目所需的包和库
├── Main.py                 # 项目唯一启动文件
├── conf                    # 项目配置文件
│   ├── account.json        # 可用的一站式账户
│   ├── database.json       # 项目使用的数据库配置
│   └── template.*.json     # 配置文件对应的模板
├── utils                   # Python代码，工具函数
│   ├── __init__.py
│   ├── _mysql.py           # 对PyMySQL封装的简易数据库操作类
│   ├── _db_manager.py      # 数据库操作函数
│   └── _get_cookie.py      # 获取后续所需的cookies
└── get_data                # Python代码，核心过程
    ├── __init__.py
    ├── _base_info.py       # 获取基础信息
    └── _core_data.py       # 获取核心数据
```


### 7、附录
#### 7.1 项目中使用到的api地址
- 查询当前学年学期
> http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxdqxnxq.do
- 查询当前周次和总周次
> http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do
- 查询总教学周次
> http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do
- 获取教学楼信息
> http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxkxjs1.do
- 获取教室信息
> http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxkxjs1.do
- 获取指定周次的数据
> http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do
* 以上仅为简单枚举，具体用法(请求头及请求参数请参考源码及注释)
