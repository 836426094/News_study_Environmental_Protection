#coding=utf-8


import smtplib
import sys
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

class Email():
    def __init__(self):
        pass

    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode('utf-8'), addr))

    def send_Email(self,title,data,to_userlist):
        # from_addr = 'litao@ronhe.com'
        # password = 'Demon&19910831@s'

        from_addr = 'qjt@ronhe.com.cn'
        password = '15278112919@bian'
        to_addr = to_userlist  #发送的邮件群  'litao@ronhe.com'
        smtp_server = 'c2.icoremail.net'                  #邮件的服务器
        msg = MIMEText(data, 'plain', 'utf-8')
        msg['From'] = self._format_addr(from_addr)
        msg['Subject'] = Header(title, 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()