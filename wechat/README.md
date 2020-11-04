# [NjnuClassroom 南师教室](../README.md)

## 第三部分 小程序(微信小程序/QQ小程序)

### 1、简介

该部分为“南师教室”项目的客户端部分，主要用于前端数据展示，根据用户要求向服务器发送查询请求，并对接受到的响应进行处理，以指定格式呈现至用户界面。
该部分采用基于微信小程序的移动端开发模式。

### 2、开发语言及环境

项目该部分采用微信开放平台提供的集成开发环境进行开发，选用了TypeScript编程语言，遵循ES6标准。
TypeScript是由微软开发的开源跨平台编程语言，作为JavaScript的超集，TypeScript添加了可选的静态类型系统，以及类、接口、模块、命名空间等。相较于JavaScript，TypeScript更适合于大型项目的开发和维护。

### 3、构建方法

项目该部分采用npm构建，初始化时通过以下命令安装依赖：
> npm install

编译命令为
> npm run tsc

### 4、项目结构

```Markdown
├── tsconfig.json           # TypeScript配置文件
├── project.config.json     # 小程序配置文件
├── package.json            # npm配置文件
├── node_modules            # npm模块依赖
│   ├── miniprogram
│   ├── typescript
│   └── ...
├── typings                 # 类型定义
│   ├── types               # 基本数据类型
│   ├── index.d.ts          # 基础接口（IAppOption等）
│   └── ...                 # 其他自定义类型
└── miniprogram             # 小程序目录
    ├── app.json            # 项目配置文件
    ├── app.ts              # 全局类（全局变量、启动函数）
    ├── app.wxss            # 全局样式表
    ├── style               # weui
    │   ├── weui.wxss       # 样式表
    │   └── ...
    ├── images              # 资源文件（图片）
    ├── utils               # 
    │   ├── util.ts         # 工具模块，计算距离、节次等
    │   └── parser.ts       # 工具模块，解析数据等
    └── pages               # 小程序页面
        ├── index           # 启动页，基础功能，查询空教室
        └── searchmore      # 更多搜索，根据查询条件筛选
```
