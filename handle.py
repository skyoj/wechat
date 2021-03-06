# -*- coding: utf-8 -*-
import hashlib
import web
import receive
import reply
import kdniao

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "zifan"  # 请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is", webData
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = kdniao.get_express(recMsg.Content)
                replyMsg = reply.TextMsg(toUser,fromUser,content)
                return replyMsg.send()
            else:
                print "暂不处理"
                return "success"
        except Exception, Argment:
            return Argment
