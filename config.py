# -*- coding: utf-8 -*-
import sys
from os import uname
import datetime

import os.path
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, "3party/"))
sys.path.insert(0, os.path.join(app_root, "module/"))
sys.path.insert(0, os.path.join(app_root, "web/"))
#   指定的模板路径
JINJA2TPL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__)
        , "templates/")
    )

#import hashlib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 全局值
class Borg():
    '''base http://blog.youxu.info/2010/04/29/borg
        - 单例式配置收集类
    '''
    __collective_mind = {}
    def __init__(self):
        self.__dict__ = self.__collective_mind
    
    VERSION = "echo4wx v15.9.8.2222"
    
    #管理员邮箱列表
    ADMIN_EMAIL_LIST = ['zoomquiet+gdg@gmail.com']

    if 'SERVER_SOFTWARE' in os.environ:
        # SAE
        AS_SAE = True
    else:
        # Local
        AS_SAE = False
    from sae.storage import Bucket
    BK = Bucket('bkup')


    import sae.kvdb
    KV = sae.kvdb.KVClient()
    #   系统索引名-UUID 字典; KVDB 无法Mongo 样搜索,只能人工建立索引
    K4D = {'incr':"SYS_TOT"     # int
        ,'acc':"SYS_wx_token"   # {"access_token":"ACCESS_TOKEN"
                                #  ,"expires_in":time.time()+有效时间 }
        #,'p':"SYS_pubs_ALL"    # [] 所有 文章 (包含已经 del 的)
        ,'00':"SYS_00_ALL"     # 特殊含义索引定义
        ,'11':"SYS_11_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'12':"SYS_12_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'13':"SYS_13_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'14':"SYS_14_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'15':"SYS_15_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'21':"SYS_21_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'22':"SYS_22_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'23':"SYS_23_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'24':"SYS_24_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'25':"SYS_25_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'31':"SYS_31_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'32':"SYS_32_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'33':"SYS_33_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'34':"SYS_34_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'35':"SYS_35_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'36':"SYS_36_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        ,'37':"SYS_37_ALL"     # [] 有效栏目文章 (不含已经 del 的)
        #,'e':"SYS_eves_ALL"     # [] 所有 活动 (包含已经 del 的)
        ,'his':"SYS_node_HIS"   # [] 所有 节点的K索引 (包含已经 del/覆盖 的)
    }

    GOBJMAP = {'his':'_{timestamp}_his{tot}'
        #,'tag':'t_%(timestamp)s_TAG%(tot)d'
        ,'bk':'bk_{timestamp}_ST{tot}_{name}'
        #,'p':'p_%(timestamp)s_PUB%(tot)d'
        ,'menu':'{menu}_{timestamp}_PUB{tot}'
        #,'fw':'fw_%(timestamp)s_PUB%(tot)d'
        }
    ESSAY_TAG_KEYS = ['11','12', '13', '14', '15',  
        '21', '22', '23', '24', '25', 
        '31', '32', '33', '34','35','36','37'
        ]

    # for show in wx echo
    _PRE20 = u'''杨早编"话题"已有十年,回头看,往前看,好多文章值得一看,再看'''
    _PRE30 = u'''"阅读邻居"是绿茶,邱小石,杨早创办的读书会,一年十期'''
    ESSAY_TAG = {'11':u''' 介读 ~ 
             致力于向别人推介各种读物,纸书,电影,网文,音乐,有介无类
            '''
        , '12':u''' 论世 ~ 
            论与当下生活相关的一切，世相，人情，俗话，新事
            '''
        , '13':u''' 讲史 ~ 
            讲述历史的各种趣闻，八卦，人人都爱好故事
            '''
        , '14':u''' 记事 ~ 
            杨早自己的生活与回忆，还包括两周一篇的“傻子镇同步“
            '''
        , '15':u''' 衡文 ~ 
            应邀点评一些中学生的作文，在“应试”与“文章”两类标准之间切换
            '''
        , '21':u'''%s #综述# ~ 
            杨早每年都会写一篇年度综述,梳理当年中国社会精神脉络 
            '''% _PRE20
        , '22':u'''%s #文化# ~ 
            这是1217俱乐部本色当行
            '''% _PRE20
        , '23':u'''%s #教育# ~ 
            我们是这样被教大的,我们希望我们的孩子还这样吗?
            '''% _PRE20
        , '24':u'''%s #社会# ~ 
            其实是把社会热点事件当作文本来读,世界是一本大书
            '''% _PRE20
        , '25':u'''%s #观影# ~ 
            私人影评
            '''% _PRE20
        , '31':u'''%s 
        荐书 ~ 
            每期读书会,我们都会让每个参与者推荐一至两本书. 由于自由报名,参与者无可预知,因此书单也千奇百怪,无所不包
            '''% _PRE30
        , '32':u'''%s 
        主题 ~ 
            每期会指定一本或多本主题书,参与者必须读过+发言,这些发言,也是让人脑洞大开
            '''% _PRE30
        , '33':u'''%s 
        DIAO ~ 
            一个盲拍式的游戏. 三个创始人各推荐一本书,不透露书名,挂在读易洞网店打包出售,附赠微刊一份,包括当月阅读邻居荐书单,还有三名创始人的荐书大PK
            '''% _PRE30
        , '34':u'''%s 
        洞见 ~ 
            读易洞是阅读邻居的大本营,要开会要议事,就在群里吆喝一声"洞见",将来我们把各种讨论描述赞美吐槽编印成书,也会叫"洞见"
            '''% _PRE30
        , '35':u'''%s 
        互推 ~ 
            与别的公号或者人物的推介 
            '''% _PRE30
        , '36':u'''%s 
        来瞧 ~ 
            讲座预告，活动记录，报道访谈.
            '''% _PRE30
        , '37':u'''%s 
        征稿 ~ 
            向关注者征集稿件.
            '''% _PRE30
        }




    #KEY4_incr = K4D['incr']
    for k in K4D:
        if None == KV.get(K4D[k]):
            if 'incr' == k:
                KV.add(K4D[k], 0)
            else:
                KV.add(K4D[k], [])
    '''
            elif 'fw' == k:
                KV.add(K4D[k], {'sequence':[]})
    '''

    # 文章索引 ESSAY_TAG_ID+code >> 文章索引号
    K4WD = {"uuid":""
        , "his_id":""   # 更新戮
        , "del":0
        , "type":"txt"  # 信息类型 txt|uri|pic
        , "tag":"ot"
        , "code":""     # 文章,分类序号
        , "news":[]     # 支持最多10个的图文
        }
    K4new = {'title':''
        , "desc":""     # 解释
        , "pic":''
        , "uri":""
        }
        
        


    #   历史操作 键-名字典
    K4H = {'C':"Create"
        ,'D':"Delete"
        ,'U':"Update"
        }
    #'uuid':""     # 历史版本扩展ID
    objHis = {'hisobj':""
        ,'actype':"..."     # 操作类型C|D|U~ Create|Delet|Update = 创建|删除|更新
        ,'dump':''        # 数据集
        }



    #__alltags = ''.join(ESSAY_TAG_KEYS)
    #print __alltags
    CMD_TPLS = {'hH?': 'TXT_HELP'
        , 'vVlog':'TXT_VER'
        , 'sS':'TXT_PLS_TAG'
        }
    CMD_ALIAS=('h', 'H', 'help', '?'    # 帮助
        , 'v', 'V', 'version', 'log'    # 版本
        , 's', 'S'                      # 文章检索
        #   隐藏功能:::
        #, 'st', 'stat'                  # 系统状态
        #, 'nn'                          # 牛妞日记
        )

    # for CLI local usage
    TPL_SUBS='''<xml>
    <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
    <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
    <CreateTime>%(tStamp)s</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[%(content)s]]></Event>
    </xml>'''
    TPL_CLICK='''<xml>
    <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
    <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
    <CreateTime>%(tStamp)s</CreateTime>
    <MsgType><![CDATA[CLICK]]></MsgType>
    <Event><![CDATA[%(content)s]]></Event>
    </xml>'''
    TPL_TEXT='''<xml>
    <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
    <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
    <CreateTime>%(tStamp)s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%(content)s]]></Content>
    </xml>'''

    TPL_URIS='''<xml>
    <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
    <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
    <CreateTime>%(tStamp)s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>%(item_count)d</ArticleCount>
    <Articles>
    %(items)s
    </Articles>
    </xml> 
    '''

    TPL_ITEM='''<item>
    <Title><![CDATA[%(title)s]]></Title> 
    <Description><![CDATA[%(description)s]]></Description>
    <PicUrl><![CDATA[%(picurl)s]]></PicUrl>
    <Url><![CDATA[%(url)s]]></Url>
    </item>
    '''



    TXT_VER = u'''阅读邻居(杨早) 公众号服务系统:
    - 版本:%s

    Changelog:
    - 150207 追加子菜单 互推
    - 150206 修订返回文字,精减以免超时
    - 150204 进一步 精减为 杨早公众号使用 
    - 150125 开始为 蠎中国 精减/定制 
    - 130928 启用Storage 服务,数据可备份/下载/恢复
    - 130926 启用 Jeff 的SDK,配合运营CLI 工具简化代码
    - 130923 初始可用,并发布 42分钟乱入 wechat 手册!-)
    - 130918 为 珠海GDG 启动开发

    更多细节,请惯性地输入 h 继续吧 :)'''% VERSION

    TXT_HELP = u'''阅读邻居(杨早) 公众号目前支持以下命令:
    s   ~ 查阅文章
    h   ~ 使用帮助
    V   ~ 系统版本
    '''
    TXT_WELCOME = u'''阅读邻居(杨早) 公众号目前支持以下命令:
    s   ~ 查阅文章
    h   ~ 使用帮助
    V   ~ 系统版本
    功能正在完善中，欢迎反馈。
    更多细节,请惯性地输入 h 继续吧 :)
    '''
    TXT_THANX = u'''亲! 感谢反馈信息, 大妈们得空就回复 ;-)
    '''


    PAPER_TAGS = ESSAY_TAG.keys()
    TXT_TAG_DEFINE = "    ".join([u"%s %s\n"%(k, ESSAY_TAG[k]) for k in ESSAY_TAG_KEYS])

    TXT_PUB_WAIT = u'''对不起亲!
    过往文章的信息,大妈们还没来的及增补进来,
    放轻松,等等先... (~.~)

    更多细节,请惯性地输入 h 继续吧 :)
    '''
    TXT_PLS_TAG = u'''亲! 请输入文章类别编码(类似 dm 的2字母):
    然后,俺才能给出该类别的文章索引...

    %s

    也可以输入 q 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''% TXT_TAG_DEFINE

    TXT_OUT_TAG = u'''亲! 目测输错了类别编码,再试?
    (类似 dm 的字串):

    %s

    也可以输入 q 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''% TXT_TAG_DEFINE

    TXT_TAG_PAPERS = u'''%s ::

    %s

    可输入 q 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_PLS_INT = u'''亲! 请输入类型文章的编号,仅数字就好:

    也可以输入 q 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_PUB_LIST = u'''%s ::
    %s

    也可以输入 q 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''





    APIPRE = "/cli" #% _API_ROOT
    STLIMI = 4.2    # 请求安全时限(秒)
    SECURE_ARGS = ('appkey', 'ts', 'sign')
    CLI_MATTERS = {     # 命令行响应方式速查字典
        "his/last":   "GET"       # 最后一次节点(任意)修订
        , "echo":       "GET"       # 模拟wechat 问答
        , "subs":       "GET"       # 模拟wechat 关注
        , "clic":       "GET"       # 模拟wechat 菜单
        , "info":       "GET"       # 查阅 指定 信息
        , "get/acc":    "GET"       # 查阅 指定 信息
        , "find/m":     "GET"       # 搜索用户
        , "del/usr":    "DELETE"    # 软删除所有用户 (包含tag 信息)
        , "reliv/usr":  "PUT"       # 恢复指定用户
        , "acl/usr":    "PUT"       # 设置用户权限
        , "ls/usr":   "GET"       # 列出指定级别用户

        , "fix/dm":     "PUT"       # 修订 大妈 信息
        , "fix/m":      "PUT"       # 修订 成员 信息
        , "fix/e":      "PUT"       # 增补 活动 信息
        , "fix/p/fv":   "PUT"       # 增补 gb文章 信息
        , "fix/p/dl":   "PUT"       # 增补 dd文章 信息
        , "fix/p/es":   "PUT"       # 增补 gt文章 信息
        , "fix/p/ac":   "PUT"       # 增补 dm文章 信息
        , "fix/p/it":   "PUT"       # 增补 hd文章 信息
        , "fix/p/ot":   "PUT"       # 增补 其它文章 信息

        , "sum/p/fv":   "GET"       # 统计 分类文章 信息现状
        , "sum/p/dl":   "GET"       # 统计 分类文章 信息现状
        , "sum/p/es":   "GET"       # 统计 分类文章 信息现状
        , "sum/p/ac":   "GET"       # 统计 分类文章 信息现状
        , "sum/p/it":   "GET"       # 统计 分类文章 信息现状
        , "sum/p/ot":   "GET"       # 统计 分类文章 信息现状
        , "sum/his":    "GET"       # 统计 历史 索引现状
        , "sum/db":     "GET"       # 统计 整体 信息现状
        , "sum/dm":     "GET"       # 统计 大妈 信息现状
        , "sum/m":      "GET"       # 统计 成员 信息现状
        , "sum/e":      "GET"       # 统计 活动 信息现状
        , "sum/p":      "GET"       # 统计 文章 信息现状
        , "del/p":      "DELETE"    # 删除指定文章

        
        , "st/kv":      "GET"       # 查阅 KVDB 信息
        
        , "push/p":     "POST"      # 推送批量文章数据 可以根据 url 判定是否有重复 

        , "sum/bk":     "GET"       # 综合 备份 数据现状
        , "del/bk":     "DELETE"    # 删除指定备份 dump

        , "bk/db":    "POST"      # 备份整个 KVDB
        , "bk/dm":    "POST"      # 备份所有 大妈
        , "bk/m":     "POST"      # 备份所有 成员
        , "bk/e":     "POST"      # 备份所有 活动
        , "bk/p":     "POST"      # 备份所有 文章

        , "revert/db":  "PUT"      # 恢复整个 KVDB
        , "revert/dm":  "PUT"      # 恢复 大妈 数据
        , "revert/m":   "PUT"      # 恢复 成员 数据
        , "revert/e":   "PUT"      # 恢复 活动 数据
        , "revert/p":   "PUT"      # 恢复 文章 数据

        , "resolve/his": "PUT"     # 重建 HIS 索引
        , "resolve/wx":  "PUT"     # 重建 wx_Passpord-->UUID 索引
        , "resolve/fw": "PUT"      # 重建 FW 索引容器,从旧的 [] -> {}

        , "wx/t":       "HTTPS"     # 获取 token
        , "wx/ls":      "HTTPS"    # 获取关注列表
        , "wx/usr":     "HTTPS"     # 获取 用户信息
        , "wx/msg":     "HTTPS"     # 获取 用户信息

        , "sum/fw":     "GET"     # 获取 转抄 状态
        , "fw/ll":      "GET"     # 模拟 大妈 刷转抄
        , "fw/dd":      "GET"     # 模拟 订户 刷回复
        , "fw/mm":  "PUT"     # 忽略 订户 消息
        , "fw/aa":  "PUT"     # 转复 订户 消息

        }

    CLI_URI = {     # 命令行 请求外部系统URI 速查字典
        "wx/t":     ("api.weixin.qq.com"
            , "/cgi-bin/token?grant_type=client_credential&appid=%(appid)s&secret=%(secret)s"
            )     # 获取 token
        , "wx/ls":  ("api.weixin.qq.com"
            , "/cgi-bin/user/get?access_token=%(token)s"
            )     # 获取关注列表
        , "wx/usr": ("api.weixin.qq.com"
            , "/cgi-bin/user/info?access_token=%(token)s&openid=%(openid)s"
            )     # 获取成员信息
        , "wx/msg": ("api.weixin.qq.com"
            , "/cgi-bin/message/custom/send?access_token=%(token)s"
            , "POST")     # 发送消息
        }
    #https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=ACCESS_TOKEN

    LEVEL4USR = {"mana":0
        , "up":1
        , "api":2
        }



    
CFG = Borg()
print CFG.VERSION

