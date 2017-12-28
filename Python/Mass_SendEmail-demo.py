#!/usr/bin/env python
#-*- coding:utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def send_mail(title, content):
    from_user = '138@139.com'
    to_user = '收件人'
    from_addr = '138@139.com'
    password = '******'
    to_addr = 'deniss.wang@gmail.com,9935226@qq.com'
    smtp_server = 'smtp.139.com',
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = _format_addr(from_user+' <%s>' % from_addr)
    msg['To'] = _format_addr(to_user+' <%s>' % to_addr)
    msg['Subject'] = Header(title, 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(0)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr.split(','), msg.as_string())
    server.quit()
if __name__=="__main__":
    subject = '测试'
    body = '<h2>内容:</h2><h4>Hello,World!</h4>'
    send_mail(subject, body)

