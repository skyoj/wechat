# !/usr/bin/python
# encoding:utf-8

import json
import urllib
import urllib2
# import urllib.request
import hashlib
import base64
import urlparse

# 此处为快递鸟官网申请的帐号和密码
# APP_id = "1266271"
# APP_key = "7526a46e-3a2a-4f5b-8659-d72f361e3386"
APP_id = "1274454"
APP_key = "a200ce9f-e005-4e77-84ec-fe47498ee6fe"


def encrypt(origin_data, appkey):
    """数据内容签名：把(请求内容(未编码)+AppKey)进行MD5加密，然后Base64编码"""
    m = hashlib.md5()
    m.update((origin_data+appkey).encode("utf8"))
    encodestr = m.hexdigest()
    base64_text = base64.b64encode(encodestr.encode(encoding='utf-8'))
    return base64_text


def sendpost(url, datas):
    """发送post请求"""
    # postdata = urllib.parse.urlencode(datas).encode('utf-8')
    postdata = urllib.urlencode(datas).encode('utf-8')
    header = {
        "Accept": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept-Encoding": "utf-8"
    }
    # req = urllib.request.Request(url, postdata, header)
    req = urllib2.Request(url, postdata, header)
    get_data = (urllib2.urlopen(req).read().decode('utf-8'))
    return get_data


def get_company(logistic_code, appid, appkey, url):
    """获取对应快递单号的快递公司代码和名称"""
    data1 = {'LogisticCode': logistic_code}
    d1 = json.dumps(data1, sort_keys=True)
    requestdata = encrypt(d1, appkey)
    post_data = {
        'RequestData': d1,
        'EBusinessID': appid,
        'RequestType': '2002',
        'DataType': '2',
        'DataSign': requestdata.decode()}
    json_data = sendpost(url, post_data)
    sort_data = json.loads(json_data)
    return sort_data


def get_traces(logistic_code, shipper_code, appid, appkey, url):
    """查询接口支持按照运单号查询(单个查询)"""
    data1 = {'LogisticCode': logistic_code, 'ShipperCode': shipper_code}
    d1 = json.dumps(data1, sort_keys=True)
    requestdata = encrypt(d1, appkey)
    post_data = {'RequestData': d1, 'EBusinessID': appid, 'RequestType': '1002', 'DataType': '2',
                 'DataSign': requestdata.decode()}
    json_data = sendpost(url, post_data)
    sort_data = json.loads(json_data)
    return sort_data


def get_express(expresscode):
    """输出数据"""
    url = 'http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx'
    data = get_company(expresscode, APP_id, APP_key, url)
    if not any(data['Shippers']):
        return "未查到该快递信息,请检查快递单号是否有误！"
    else:
        print("已查到该", data['Shippers'][0]['ShipperName']+"("+
              data['Shippers'][0]['ShipperCode']+")", expresscode)
        trace_data = get_traces(expresscode, data['Shippers'][0]['ShipperCode'], APP_id, APP_key, url)
        if trace_data['Success'] == "false" or not any(trace_data['Traces']):
            return "未查询到该快递物流轨迹！"
        else:
            str_state = "问题件"
            if trace_data['State'] == '2':
                str_state = "在途中"
            if trace_data['State'] == '3':
                str_state = "已签收"
            print("目前状态： "+str_state)
            trace_data = trace_data['Traces']
            item_no = 1
            Linedata = []
            for item in trace_data:
                Linedata.append((str(item_no)+":", item['AcceptTime'], item['AcceptStation']))
                item_no += 1
            Msgdata = "目前状态： "+ str_state + "\n" + "\n".join(Linedata)
            print "test start kd"
            print Linedata
            print Msgdata
            return Msgdata
