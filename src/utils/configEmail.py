#-*- coding:utf-8 -*-
'''
filename : configEmail.py
create by : 
create time : 2019/07/09
introduce : 实现发送邮件功能
'''
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from utils.readConfig import readConfig as cf

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 


send_flag = cf.get_email('on_off')#发送邮件开关
serveraddrs = cf.get_email('serveraddrs')#qq邮箱的smtp地址
port = int(cf.get_email('port'))#端口
subject = cf.get_email('subject')#从配置文件中读取，邮件主题
fromaddr = cf.get_email('fromaddr')#发件人
password = cf.get_email('password')#邮件客户端授权码
toaddrs = cf.get_email('toaddrs')#收件人

 
class send_email():
    def send(self,filename):
        file_path = os.path.join(parentdir, 'report', filename)#获取测试报告路径
        content = """
                    执行测试中……
                    测试已完成！！
                    生成报告中……
                    报告已生成……
                    报告已邮件发送！！
                    """
        htmlApart = MIMEApplication(open(file_path,'rb').read())
        htmlApart.add_header('Content-Disposition','attachment',filename=filename)
        m = MIMEMultipart()
        m.attach(htmlApart)
        m.attach(MIMEText(content,'plain', 'utf-8'))
        m['Subject'] = subject
        try:
            server = smtplib.SMTP(serveraddrs,port)
            server.login(fromaddr,password)
            server.sendmail(fromaddr,toaddrs,m.as_string())
            print('success')
            server.quit()
        except smtplib.SMTPException as e:
            print('error:',e)
 

sendemail = send_email()
if __name__ == '__main__':# 运营此文件来验证写的send_email是否正确
    print(subject)
    sendemail.send('report.html')
    print("send email ok!!!!!!!!!!")
