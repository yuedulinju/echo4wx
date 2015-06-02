# echo4wx 精简公众号后台

- 仓库: [readerneighbor/echo4wx - GitCafe](https://gitcafe.com/readerneighbor/echo4wx)
- 应用: http://sayeahoo.sinaapp.com
- 参考: [42分钟乱入 wechat 手册!-) — chaos2wechat 1.1.131010 documentation](http://chaos2.qiniudn.com/wechat/build/html/)

## 功能

- 应答 wechat 后台认证请求,完成开发者模式的开启
- 基于 SAE 完成自制菜单的响应,将 KVDB 中的数据,变成微信文本返回读者
  + 通过索引号,返回过往公众号文章链接
  + 从而突破微信后台自定关键词响应的 300 个限制
- 基干远程 CLI 的数据维护

### 150204 部署

读者功能:

- h 帮助菜单
- v 版本说明
- s 文章查询:
    + 分类列表
    + 分类文章清单
    + 回复文章索引号反馈文章图文链接

运维功能:

`CLI.py` 命令行测试/开发/运维工具


    $ python CLI.py  -h
    echo4wx v15.2.13.21
    CLI for WeKnow.
    Usage:
      CLI.py [--debug] <matter> [<sets>]

    Options:
      -h --help     Show this screen.
      -V --version  Show version.
      -D --debug    对本地系统测试时专用参数
      <matter>      事务URI
      <sets>        数据设定

    e.g:
      一般形式::
      $ python CLI.py 事务指令 [可能的值设定 set=** 形式]
      详细操作::
      echo set=i                模拟微信的消息交互
      subs set=subscribe|unsubscribe
                                模拟微信的关注事件
      clic set=KEY              模拟微信的菜单交互
      info/:UUID                查阅指定 信息
      st/kv     查询 KVDB 整体现状
      sum/p/:TAG 综合 分类文章 信息现状
      get/acc     查询 access_token

      !!! 小心:大规模数据I/O操作 !!!
      push/p yaml=path/2/x.yaml 提交文章数据


- 本地使用方式参考: [150203-wechat-sae-srv-dev_480](http://v.youku.com/v_show/id_XODg1NzMyNjQw.html)
- 简单的说将所有真实系统中的所有行为,在本地完全模拟出来

**注意:**

- 以上操作录像是老版本系统的远程管理情景
- 当前阅读邻居的已经简化了维护流程
- 只通过对 `.ymal` 的维护,针对具体菜单进行整体批量替换


`具体操作:`

    $ python CLI.py  push/p yaml=yaml/35.yaml
    ...
    {
        "data": [
            "350->啥子叫做耍、朋、友",
            "351->今日耍文：有槽得吐,有书得卖,今日耍文：有槽得吐,今日耍文：有槽得吐",
            "3510->要推行《弟子规》，请用逻辑说服我,为什么《弟子规》是精神雾霾,关于“弟子规是不是精神雾霾”的评论（多图）,两代相处之道，关键在于“不评判”",
            "352->一个厨子走了，生活顿时索然无味,黯然销魂者，唯别而已矣,三哥到天堂耍去了,只要开始，就已完美,两写陈三,三爷 [黄永],三哥访谈选（2011）",
            "353->【傻子镇】傻子些，喝啥哟",
            "354->【傻子镇同步】傻3吸氧记,傻3起名字,傻3游潘家园,傻3还乡,傻3编《话题》",
            "355->【傻子镇同步】傻子没有乡愁,从辣子身上学历史,商务评书记",
            "356->明天，一起送别黄永,啤酒黄永,书与人之十二——致黄永,人人心中有个傻一",
            "357->输贱恩仇录（腾讯大家版）,你以为他是个吹风机，其实他是个剃须刀",
            "358->为了国家，为了社会，逼你结婚",
            "359->我与柴静的私人恩怨,《我与柴静的私人恩怨》的回应与补充"
        ],
        "msg": "reloaded 11 POSTs. \nin CLASS 35"
    }


- 即完成对 `读邻->互推` 菜单响应内容的维护


>"阅读邻居"是绿茶,邱小石,杨早创办的读书会,一年十期 
>        互推 ~ 
>            阅读邻居 作为知名读书品牌活动, 自然少不了帮忙相互推荐有关社区/活动/公众号 的有关文章/活动了.
>             
> 350 啥子叫做耍、朋、友
> 351 今日耍文：有槽得吐 +另4篇
> 3510 要推行《弟子规》，请用逻辑说服我 +另4篇
> 352 一个厨子走了，生活顿时索然无味 +另7篇
> 353 【傻子镇】傻子些，喝啥哟
> 354 【傻子镇同步】傻3吸氧记 +另5篇
> 355 【傻子镇同步】傻子没有乡愁 +另3篇
> 356 明天，一起送别黄永 +另4篇
> 357 输贱恩仇录（腾讯大家版） +另2篇
> 358 为了国家，为了社会，逼你结婚
> 359 我与柴静的私人恩怨 +另2篇
> 
> 
> 输入索引号可获文章链接
> (上述前缀 1446 样的纯数字)


**已知问题:**

- 纯文本的响应信息,每次最多 `1024` 字
- 所以,对多图文信息进行了压缩


### TODO

- 增补 TDD 案例
- 清除无用代码
- 进一步增补开发文档
- 尽力吻合 PEP8

## 目录结构

```
.
+- 3party               第三方模块
+- logs                 本地数据容器,一般运行时
|                 $ dev_server.py --storage-path=logs/data/ 
|                                 --kvdb-file=logs/kv.db
+- module               自制工具模块
+- templates            可能的模板收集
+- web                  真正的应用目录
+- yaml                 数据维护目录 分栏目专用文件长期增补,用 CLI 工具push 到SAE
|- CLI.py               
|- README.md            本文
|- bottle.py            内置的 web 框架,比 SAE 的版本高
|- chaos2pychina.leo    文学化编程工程文件,没有安装 Leo 的就不用打开了
|- config.py            所有全局变量
|- config.yaml          SAE 应用声明
|- index.wsgi           SAE 应用入口
|- requirements.txt     环境依赖声明
|- _pylintrc            推荐配置为 ~/.pylintrc 坚持使用
|- _xsettings.py        机密配置文件模板
`- xsettings.py         机密配置执行文件

```

## 数据设计

充分使用 `KVDB` 的特性,建立极简数据关系

```
SYS_*_* 为人工索引:
  e.g:
  SYS_dm_ALL -> [10, 11, 12,,,]

[d{2,5}] 为文章索引:
  e.g:
  2151 -> {"uuid":""
    , "his_id":""   # 更新戮
    , "del":0
    , "type":"txt"  # 信息类型 txt|uri|pic
    , "tag":"ot"
    , "code":""     # 文章,分类序号
    , "news":[{'title':''
        , "desc":""     # 解释
        , "pic":''
        , "uri":""
        }
      ,,,]     # 支持最多10个的图文
    }

```

## 记要

- 150203 ZoomQuiet 完成原型
- 150125 ZoomQuiet 构建原型
- 141111 动议
