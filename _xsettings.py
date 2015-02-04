# -*- coding: utf-8 -*-
'''本地测试用机密配置文件
- 修订相关字段的值为你的
- 将文件名也修订为 xsettings.py 即可起作用
'''
class Borg():
    '''base http://blog.youxu.info/2010/04/29/borg
        - 单例式配置收集类
    '''
    __collective_mind = {}
    def __init__(self):
        self.__dict__ = self.__collective_mind

    TO_SAE = "http://你的后台.sinaapp.com/api"
    # all kinds of security abt. set
    TOKEN =  "微信应用令牌"
    APPKEY = "微信应用专匙"
    SECRET = "微信应用安全码"

    WX_GDG = '模拟公众号'
    AS_SRV = WX_GDG
    AS_USR = "模拟用户"

XCFG = Borg()
