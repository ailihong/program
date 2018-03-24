# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 13:31:10 2018
比特币价格监测程序
@author: bai
"""
import time,threading
import json
import urllib2
import smtplib
from email.mime.text import MIMEText

class monitor(threading.Thread):
    def __init__(self,time_period=1):#定时周期
        super(monitor, self).__init__()
        print 'init ...'
        self.time_period = time_period
        self.last_change_24h=self.get_price()
        self.cur_change_24h=self.last_change_24h
        
    
    def get_price(self):
        get_url='https://api.coinmarketcap.com/v1/ticker/bitcoin/'
        headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        request=urllib2.Request(get_url,headers=headers)
        #获得回送的数据
        response=urllib2.urlopen(request)#如果后台没有立即给返回值，则阻塞等待
        ret = response.read()
        text = json.loads(ret)
        price=float(text[0]['percent_change_24h'])
#        print price
        return price
        
    def push_mail(self):
        msg_from='makeitbai@qq.com'#发送方邮箱
        passwd='kwnxqkwebnyvfcig'#填入发送方邮箱的授权码
        msg_to='make_it_bai@foxmail.com'#收件人邮箱
        subject="BTC 24h变化率下降通知"#主题     
        content='last 24h change:%s, now 24h change:%s'%(self.last_change_24h,self.cur_change_24h)#正文
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com",465)#邮件服务器及端口号
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
#            print "发送成功"
        except s.SMTPException,e:
            pass
        finally:
            s.quit()
    def run(self):#重写父类run方法，在线程启动后执行该方法内的代码
       while True:
           self.cur_change_24h=self.get_price()
           if self.cur_change_24h < self.last_change_24h:
               self.push_mail()
           time.sleep(self.time_period)
           self.last_change_24h=self.cur_change_24h
           
if __name__ == '__main__':
    moni=monitor(20)
    moni.start()
    moni.join()
