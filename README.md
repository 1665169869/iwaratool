# IwaraTool

## 介绍

还没有详细的介绍，因为还在测试阶段 希望大家可以和我一起维护这个项目
目前最简单的json文件都有四十多kb 这还是只带上了视频id和url下载地址之类的

### 目前版本：**0.1.0**

### 关于debug变量：

目前只是暂时使用print来分辨执行到哪里了

后续会重写整个debug（不是我不会.ing）

## 开源协议
[Apache License 2.0](/LICENSE)

## 如何安装

运行目录下的 [setup.py](/setup.py)

> python [setup.py](/setup.py) build

或者使用pip

> pip install iwaratool

## 更新日志

### 0.1.0: 

刚刚诞生 只有一个userVideos半成品

### 0.1.1:

1. 改进了json输出的格式
2. 改进了userVideos函数
3. 添加了debug输出（未完成），添加了title_all（未完成）<br>
也添加了一堆的bug和未完成


## 文件结构

+ iwaratool
    - \_\_init\_\_.py
    - search.py
    - setting.py
    - user.py

user.py：

爬取用户内容

searc.py：

爬取搜索到的内容

setting：

一键编辑个人信息

制作优先级从上往下

### json结构

根对象：
|字段|类型|内容|
|-|-|-|
|videos|obj|信息本体|

videos对象：
|字段|类型|内容|
|-|-|-|
|pages|int|总页数 从0开始|
|data|list|数组信息本体|

data对象：
|字段|类型|内容|
|-|-|-|
|code|int|状态码 一般为200|
|name|str|用户名称|
|title|str|标题|
|id|str|视频ID|
|like|str|收藏人数|
|look|str|观看人数|
|url|str|视频地址|
|covers|str|视频封面|
|down|obj|下载地址信息本体|

down对象：

|字段|类型|内容|
|-|-|-|
|code|int|状态码 一般为200|
|data|list|数组信息本体|

down.data对象：
|字段|类型|内容|
|-|-|-|
|resolution|str|清晰度 一般最多只有三个清晰度：<br>Source 540p 360p
|uri|str|下载地址 注意是uri不是url|
|mime|str|视频类型|