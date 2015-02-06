# -*- coding: utf-8 -*-
TPL_IDX_CLASS = u'''{tag_info}
请输入文章索引号 (类似 151 的纯数字):
然后,俺就能告诉您文章链接呢...

{idx_news}

更多细节,请惯性地输入 h 继续吧 :)
'''
TPL_IDX_LOST = u'''{tag_info}
但是...
历史文章还未整理好
傻z 受命折腾中,敬请期待 눈_눈

更多细节,请惯性地输入 h 继续吧 :)
'''
import os
#关闭fetchurl，让httplib直接使用socket服务来连接
os.environ['disable_fetchurl'] = "1" 
import sys   
import time #import time, gmtime, strftime, localtime
from datetime import datetime
import traceback
import httplib
import urllib 
import urllib2
# 打开urllib2的debug开关
urllib2.install_opener(urllib2.build_opener(urllib2.HTTPSHandler(1)))

import hashlib
import json
import string
import base64
import cPickle
#import ConfigParser
from os.path import splitext as os_splitext
from os.path import exists as os_exists

from copy import deepcopy
import xml.etree.ElementTree as etree


from auth import _query2dict, _chkQueryArgs

from utility import INCR4KV as __incr
from utility import TSTAMP, GENID, USRID, DAMAID
from utility import ADD4SYS
from utility import PUT2SS

from utility import WxApp
import yaml

import pyfsm
from pyfsm import state, transition

#from wechat.official import WxApplication, WxRequest, WxTextResponse, WxNewsResponse, WxArticle
from wechat.official import WxApplication
from wechat.official import WxRequest, WxTextResponse
from wechat.official import WxNewsResponse, WxArticle

from bottle import *
from bottle import __version__ as bottleVer
#from bottle import jinja2_template as template


#print sys.path
from config import CFG
from xsettings import XCFG
KV = CFG.KV #sae.kvdb.KVClient(debug=1)
BK = CFG.BK
debug(True)

APP = Bottle()

# echo for RESTful remote actions
'''
- 全部基于: `/api/cli` 前缀
    - 版本区隔为: `/api/v2/cli` 前缀
- 签名检验
- 时间检验(4.2秒以内, 并发不得超过 `N` 次)
'''

# collection wechat papers mana. matters
'''
'''
def _load_news(crt_tag, crt_key, crt_var, multi=False):
    uuid = GENID(crt_tag, name='menu')
    #print uuid
    #return None
    new_paper = deepcopy(CFG.K4WD)
    new_paper['uuid'] = uuid # 对象创建时, 变更时间戳同 UUID
    new_paper['his_id'] = uuid
    new_paper['lasttm'] = time.time()
    new_paper['tag'] = crt_tag
    new_paper['code'] = crt_tag+crt_key
    #CFG.ESSAY_TAG_ID[crt_tag]+crt_key
    #print new_paper['code']
    if multi:
        # mulit news
        #print crt_var
        new_paper['news'] = [{'title':i['title']
            , 'uri':i['uri']
            , 'pic':i['img']
            } for i in crt_var]
        #print new_paper['news']
    else:
        # sinle news
        #print crt_var
        new_paper['news'] = [{'title':crt_var['title']
            , 'uri':crt_var['uri']
            , 'pic':crt_var['img']
            }]
    KV.add(new_paper['code'], new_paper)
    ADD4SYS(crt_tag, new_paper['code'])
    return uuid


@APP.post('/cli/push/p/<qstr>')
def push_papers(qstr):
    q_dict = _query2dict(qstr)
    q_form = request.forms
    q_file = request.files.get('yaml')

    if _chkQueryArgs("/cli/push/p", q_dict, "POST"):
        feed_back = {'data':[], 'msg':''}
        _yaml = q_file.file.read()
        set_var = yaml.load(_yaml) #q_file.file.read()
        _tg = set_var.keys()[0]        
        for i in KV.get(CFG.K4D[_tg]):
            #print 
            KV.delete(i)

        KV.set(CFG.K4D[_tg],[])

        #return None
        #f_name, f_ext = os_splitext(q_file.filename)
        count = 0
        for k in set_var[_tg].keys():
            count += 1
            if isinstance(set_var[_tg][k], dict):
                # single news
                _load_news(_tg, k, set_var[_tg][k])
                
            elif isinstance(set_var[_tg][k], list):
                # mulit-news
                _load_news(_tg, k, set_var[_tg][k], multi = True)
                #data.append(KV.get_info())
            else:
                pass
        feed_back['msg'] += "reloaded %s POSTs. \nin CLASS %s"% (count, _tg)
        feed_back['data'].append(KV.get_info())

        _append = []
        for i in KV.get(CFG.K4D[_tg]):
            #print ['%s->%s'%(i,j['title']) for j in KV.get(i)['news']]
            _append.append('%s->%s'%(i
                , ",".join([j['title'] for j in KV.get(i)['news']])
                ))

        feed_back['data'] = _append



        return feed_back
    else:
        return "alert quary!-("



@APP.get('/cli/sum/p/<tag>/<qstr>')
def st_p_tag(tag, qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/sum/p/%s"% tag, q_dict, "GET"):
        feed_back = {'data':[]}
        #print tag
        all_papers = KV.get(CFG.K4D[tag])
        #print all_papers
        for i in all_papers:
            #print ['%s->%s'%(i,j['title']) for j in KV.get(i)['news']]
            _node = KV.get(i)
            _info = '''%s > %s: [%s]
                '''%(i
                    , _node['code']
                    , ','.join([j['title'] for j  in _node['news']])
                    )
                
            feed_back['data'].append(_info)
        return feed_back
        
    else:
        return "alert quary !-("

@APP.get('/cli/info/<uuid>/<qstr>')
def info_kv(uuid, qstr):
    '''查询 UUID 的信息
    '''
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/info/%s"% uuid, q_dict, "GET"):
        feed_back = {'data':[]}
        print "info_kv()>>> ",uuid
        print KV.get(uuid)
        #return KV.get(uuid)
        feed_back['msg'] = "safe quary;-)"
        feed_back['data'] = KV.get(uuid)
        return feed_back
    else:
        return "alert quary!-("

@APP.get('/cli/st/kv/<qstr>')
def st_kv(qstr):
    '''查询 KVDB 整体现状
    '''
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/st/kv", q_dict, "GET"):
        feed_back = {'data':[]}
        #data.append(KV.get_info())
        return KV.get_info()
        feed_back['msg'] = "safe quary;-)"
        feed_back['data'] = KV.get_info()
        return feed_back
    else:
        return "alert quary!-("

@APP.get('/cli/get/acc/<qstr>')
def get_acc(qstr):
    '''定期获得 access_token
    '''
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/get/acc", q_dict, "GET"):
        print XCFG.access
        import requests
        r = requests.get(XCFG.access)
        _json = json.loads(r.text)
        _acc = {}
        _acc['access_token'] = _json['access_token']
        _acc['expires_in'] = time.time()+int(_json['expires_in'])
        KV.set(CFG.K4D['acc'],_acc)
        return KV.get(CFG.K4D['acc'])
    else:
        return "alert quary!-("
    
@APP.get('/echo')
@APP.get('/echo/')
def echo_wechat():
    '''wechat app token echo
    '''
    #print request.query.keys()
    #print request.query.echostr
    #print request.query_string
    #print dir(BaseRequest.query_string)
    return request.query.echostr
    #return app = WxApplication.process(request.query, None)
    

'''
def wechat(request):
    app = EchoApp()
    result = app.process(request.GET, request.body, token='your token')
    return HttpResponse(result)
'''

@APP.post('/echo/')
@APP.post('/echo')
def wechat_post():
    # usage jeff SDK for wechat...
    #print request.query
    #print request.query_string
    #print request.forms
    if CFG.AS_SAE:
        #wxa = WxApplication.process(request.GET, request.body)
        wxa = WxApplication(token=XCFG.TOKEN)
        chkwx = wxa.is_valid_params(request.query)
        if not chkwx:
            return None
    else:
        print "Debugging localhost..."
    ## 注意! 从公众号来的消息和订阅号完全不同的,需要另外解析!
    #print "request.forms.keys()[0]\t\n", request.forms.keys()[0]
    wxreq = WxRequest(request.forms.keys()[0])
    if 'text' == wxreq.MsgType:
        cmd = wxreq.Content
        if cmd.isdigit():
            #print cmd
            if cmd in CFG.ESSAY_TAG_KEYS:
                #print "ESSAY_TAG_KEYS", cmd
                return _wx_echo_idx(wxreq, cmd)
            else:
                return _wx_echo_cnt(wxreq, cmd)
        else:
            if cmd in CFG.CMD_ALIAS:
                return _wx_echo_cmd(wxreq, cmd)
            else:
                return WxTextResponse(CFG.TXT_HELP, wxreq).as_xml()
                #print cmd

            #if 8 > len(crt_usr['msg']):
            #print cmd


    elif 'event' == wxreq.MsgType:
        #print wxreq.Event
        print wxreq.EventKey

        return _wx_echo_idx(wxreq, wxreq.EventKey)

        #return None
        #WxTextResponse(CFG.TXT_HELP, wxreq).as_xml()


    elif 'CLICK' == wxreq.MsgType:
        _TAG_PAPERS = '''%s :
        %s
        '''
        return WxTextResponse(_TAG_PAPERS%( 'tag'
                ,'LIST' )
            , wxreq).as_xml()

                
    return None
    



def _wx_echo_cnt(wxreq, cmd):
    print "_wx_echo_cnt", cmd
    _items = KV.get(str(cmd))
    #print _items
    #return None
    resp = WxNewsResponse(
            [WxArticle(p['title']
                ,Description=""
                ,Url=p['uri']
                ,PicUrl=p['pic']) for p in _items['news']]
            , wxreq).as_xml()

    return resp
    #return WxTextResponse(CFG.TXT_HELP, wxreq).as_xml()
def _wx_echo_idx(wxreq, cmd):
    print "_wx_echo_idx", cmd
    all_papers = KV.get(CFG.K4D[cmd])
    #print 
    all_papers.sort()
    #print len(all_papers)
    #print CFG.ESSAY_TAG[cmd]
    if 0 == len(all_papers):
        #_exp = TPL_IDX_LOST.format( tag_info = CFG.ESSAY_TAG[cmd])
        #u"但是...历史文章还未整理索引起来,敬请期待 눈_눈"
        return WxTextResponse(TPL_IDX_LOST.format( tag_info = CFG.ESSAY_TAG[cmd])
                , wxreq).as_xml()
    else:
        _exp = ""
        for i in all_papers:
            #print ['%s->%s'%(i,j['title']) for j in KV.get(i)['news']]
            _node = KV.get(i)
            if 1 == len(_node['news']):
                _exp += u"%s: %s \n"%(_node['code']
                    , _node['news'][0]['title']
                    )
            else:
                #'\n\t+'.join([j['title'] for j  in _node['news']])
                _exp += u"%s: %s +另 %s 篇\n"%(_node['code']
                    , _node['news'][0]['title']
                    , len(_node['news'])
                    )
        #print _exp
        #return None
        return WxTextResponse(TPL_IDX_CLASS.format(idx_news = _exp
                    , tag_info = CFG.ESSAY_TAG[cmd]
                ), wxreq).as_xml()


def _wx_echo_cmd(wxreq, cmd):
    for k in CFG.CMD_TPLS.keys():
        if cmd in k:
            print CFG.CMD_TPLS[k]
            _TPL = eval('CFG.%s'% CFG.CMD_TPLS[k])
            #print type(_TPL)
            #print type(CFG.TXT_HELP)
            return WxTextResponse(_TPL, wxreq).as_xml()
    #return None
    return WxTextResponse(CFG.TXT_HELP, wxreq).as_xml()
@APP.route('/sysincr')
#@APP.route('/<ddd>/sysincr')
def sysincr():
    from utility import INCR4KV as __incr
    #kv = sae.kvdb.KVClient()
    #print  kv.get_info()
    return str(__incr())




#@view('404.html')
@APP.error(404)
def error404(error):
    return '''


\          SORRY            /
 \                         /
  \    This page does     /
   ]   not exist yet.    [    ,'|
   ]                     [   /  |
   ]___               ___[ ,'   |
   ]  ]\             /[  [ |:   |
   ]  ] \           / [  [ |:   |
   ]  ]  ]         [  [  [ |:   |
   ]  ]  ]__     __[  [  [ |:   |
   ]  ]  ] ]\ _ /[ [  [  [ |:   |
   ]  ]  ] ] (#) [ [  [  [ :===='
   ]  ]  ]_].nHn.[_[  [  [
   ]  ]  ]  HHHHH. [  [  [
   ]  ] /   `HH("N  \ [  [
   ]__]/     HHH  "  \[__[
   ]         NNN         [
   ]         N/"         [
   ]         N H         [
  /          N            \

/                           \

roaring zoomquiet+404@gmail.com
'''
#    return template('404.html')

@APP.route('/favicon.ico')
def favicon():
    abort(204)
    
@APP.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')
    






