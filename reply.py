# -*- coding: utf-8 -*-
import time

class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self._dict = dict()
        self._dict['ToUserName'] = toUserName
        self._dict['FromUserName'] = fromUserName
        self._dict['CreateTime'] = int(time.time())
        self._dict['Content'] = content
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self._dict)