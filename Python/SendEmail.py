#!/usr/bin/env python
# -*- coding: utf-8 -*-
# deniss.wang
# Send Email for office365 Email
import smtplib  
from email.mime.text import MIMEText  # 引入smtplib和MIMEText

def SendMail(Email):
    host = 'smtp.office365.com'  # 设置发件服务器地址
    port = 587  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式 25 465 587
    sender = 'wolf7@example.com'  # 设置发件邮箱，一定要自己注册的邮箱
    pwd = '1234567'  # 设置发件邮箱的密码，等会登陆会用到
    receiver = 'deniss.wang@palmax.com' # 设置邮件接收人，这里是我的公司邮箱
    body = '<h1>Hi,How are you.</h1><h3>Deniss.wang</h3>' # 设置邮件正文，这里是支持HTML的

    msg = MIMEText(body, 'html') # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = 'Hello world' # 设置邮件标题
    msg['from'] = sender  # 设置发送人
    msg['to'] = receiver  # 设置接收人

    server = smtplib.SMTP(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
    server.starttls() # 因为office365使用的是starttls，如果是sina或者163，可以将此行代码注释
    server.login(sender, pwd)  # 登陆邮箱
    server.sendmail(sender, receiver, msg.as_string())  # 发送邮件！

SendMail('Email')
