#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019-7-3 Send Message to DingDing
# Author: Deniss.wang

import sys
import json
import requests

reload(sys)
sys.setdefaultencoding('utf8')

ops_dingdingd_token = '1'
aws_dingdingd_token = '2'
def SendMessage(msg):
    # AWS账单警报组钉钉机器人webhook
    aws_alert_url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % aws_dingdingd_token
    # OPS警报组钉钉机器人webhook
    ops_url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % ops_dingdingd_token
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = "%s " % msg
    String_textMsg = { \
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                "138"                                    #如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 0                                 #如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    AWS_ALERT = requests.post(aws_alert_url, data=String_textMsg, headers=HEADERS)
    OPS_ALERT = requests.post(ops_url, data=String_textMsg, headers=HEADERS)
    print(AWS_ALERT.text,OPS_ALERT.text)
if __name__ == '__main__':
    SendMessage("send dingding message")
