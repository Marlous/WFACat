# WFACat
## Introduction - 介绍
Weibo friends' net Deep analysis 微博用户好友人际关系网络深度分析（人脉深度为二）  

### Summary - 概要
- 你只需一个账号的授权链接、输入所要研究的对象。

- 即可得到 a）此研究对象的二度人脉 node.csv、edge.csv 文件供数据可视化软件 Gephi 使用。b）数据分析后写入数据库，可以得到更多详细信息，详见 “特性”。

- 软件产生的数据在 WFACat_data 文件夹下。

### Feature - 特性
1. 查询：
- 通过微博用户名查某用户基本信息

- 通过 uid 查某用户基本信息

- 通过微博用户名查某用户的互关好友列表及其好友信息

- 通过微博用户名查某一度好友能通过圈内二度好友认识的一度好友

- 所有一度好友信息

2. 统计：
- 总体概况：总人数、一度好友数、圈内二度好友数、二度好友数

- 能关联最多一度好友的圈内二度好友（取 10 条排序），能关联谁

- 一度好友中与其他一度好友互关最多的人（排序）、与圈内二度好友互关最多的人；分别是哪些人

- 一度好友 / 圈内二度好友 / 二度好友中认证情况统计

- 一度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端

- 圈内二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端

- 二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端

3. 推测：
- 根据统计的结果做出一些有趣的推测（如统计手机客户端型号等）。

## Requirements - 必要条件
- OS：Windows 10  
- IDE：PyCharm
- Python 3.7（64 bit）

## Usage - 用法
1. 克隆此仓库使用 IDE 运行，或直接使用 Release 文件夹中打包好的程序。

2. 使用流程：使用 `help` 命令查看帮助；使用 `conf` 命令进行配置；使用 `get` 命令获得基本数据；使用 `tocsv` 等命令生成需要的文件（详见 help 命令显示的帮助）；使用 `mysqld` 等命令查看深度分析的结果信息。

3. 软件使用效果截图（分别为使用 Gephi 分析、本软件使用界面）：
![软件使用效果截图](./README_img/图1.PNG)
![软件使用效果截图](./README_img/图2.PNG)

## Support - 支持
By Marlous

### Contact - 联系
邮箱：Goonecat@foxmail.com

## License - 版权信息
WFACat is released under the GPL license. See [LICENSE](https://github.com/Marlous/WFACat/blob/master/LICENSE) for additional details.