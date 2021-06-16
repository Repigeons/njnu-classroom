# NjnuClassroom 南师教室

## 总览

### 1、概述

本项目(NjnuClassroom, 南师教室)由 [南京师范大学 Repigeons团队](https://repigeons.github.io/) 设计并完成全栈开发，旨在为南师在校学生提供更便捷的服务。
本项目力求做到数据的实时化更新，为各位同学提供最准确可靠的教室信息，并通过智能排序算法，从多维度属性出发，计算出空教室的推荐系数，让同学们获得最优的使用体验。
本项目完全开源，采用 [`GNU General Public License v3.0` 开源许可证](./LICENSE)，我们希望能为大家提供一个思路，同时也欢迎更多的人加入到我们的社区中来，共同维护这一项目，不断优化，为尽可能多的同学提供尽可能多的帮助。再次感谢您的关心与支持。

### 2、项目结构

该项目共包含以下两个子项目：

（一）[数据服务器](server/README.md)

（二）[微信/QQ小程序](miniprogram/README.md)

### 3、子项目说明

#### （一）数据服务器

该部分为项目的后端数据服务，使用 Python 编程语言，共分为三个模块，分别为：

- 数据收集模块（Python爬虫）

> 该模块采用基于 Python 的爬虫技术，从一站式事务中心获取数据，对数据进行统一化处理并存入数据库。

- 数据服务模块（HTTP服务）

> 该模块使用 Flask 框架，为移动端小程序提供详细数据服务。

- 公告发布模块（HTTP服务）

> 该模块使用 Flask 框架，仅供管理人员发布公告信息时使用。

#### （二）微信/QQ小程序

该部分为项目的前端应用，使用 TypeScript 编程语言，采用 npm 构建方法。用于向用户展示查询数据结果。
