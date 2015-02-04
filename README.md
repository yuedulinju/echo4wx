# echo4wx 精简公众号后台

- 仓库: [readerneighbor/echo4wx - GitCafe](https://gitcafe.com/readerneighbor/echo4wx)
- 应用: http://sayeahoo.sinaapp.com

## 功能

命令驱动式应答

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
      
      !!! 小心:大规模数据I/O操作 !!!
      push/p yaml=path/2/x.yaml 提交文章数据


- 本地使用方式参考: [150203-wechat-sae-srv-dev_480](http://v.youku.com/v_show/id_XODg1NzMyNjQw.html)
- 简单的说将所有真实系统中的所有行为,在本地完全模拟出来

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
