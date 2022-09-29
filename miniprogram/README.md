# 微信小程序 @[南师教室NjnuClassroom](../README.md)

## 1、简介

该部分为项目的前端应用，主要用于前端数据展示，根据用户要求向服务器发送查询请求，并对接受到的响应进行处理，以指定格式呈现至用户界面。
该部分采用npm构建，使用了基于微信小程序的移动端开发模式。

## 2、开发语言及环境

该部分选用 `TypeScript` 编程语言，遵循 ES6 标准，使用 `VS Code` 与 `微信开发者工具` 进行开发。
TypeScript 是由微软开发的开源跨平台编程语言，作为JavaScript 的超集，TypeScript 添加了可选的静态类型系统，以及类、接口、模块、命名空间等。相较于 JavaScript，TypeScript 更适合于大型项目的开发和维护。

## 3、构建方法

该部分采用 npm 构建，初始化时通过以下命令安装依赖：
> npm install

编译命令为
> npm run tsc

## 4、项目结构

```text
├── tsconfig.json           # TypeScript 配置文件
├── project.config.json     # 小程序配置文件
├── package.json            # npm 配置文件
├── package-lock.json       # npm 配置文件
├── node_modules            # npm 模块依赖
│   ├── miniprogram
│   └── typescript
├── typings                 # 类型定义
│   ├── index.d.ts          # 基础接口（IAppOption等）
│   └── types               # 其他数据类型
│       ├── wx              # 微信定义的类型
│       └── custom          # 开发者自定义的类型
└── miniprogram             # 小程序目录
    ├── app.json            # 应用配置文件
    ├── app.ts              # 全局类（全局变量、启动函数）
    ├── app.wxss            # 全局样式表
    ├── images              # 图片资源文件
    ├── utils               # 工具包
    │   ├── util.ts         # 工具模块，计算距离、节次等
    │   ├── parser.ts       # 工具模块，解析数据等
    │   ├── getCache        # 工具模块，数据缓存与预加载
    │   └── hash            # 工具模块，哈希算法md5
    ├── components          # 自定义组件
    └── pages               # 小程序页面
        ├── empty           # 查询空教室
        ├── overview        # 教室概览
        └── explore         # 发现栏
            ├── index       # 发现页面
            ├── search      # 更多搜索
            └── shuttle     # 校车时刻表
```
