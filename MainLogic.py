#coding:utf-8
import urllib2
import re
import time
import sched
import top.api.rest.AlibabaAliqinFcSmsNumSendRequest as SmsSender
import top

SourceURL = ['http://sse.tongji.edu.cn']
InfoCenterPostfix = ['/InfoCenter/index.aspx']

class InfoController:
    LastData = ''
    LastMessage = ''
    schedule = sched.scheduler(time.time, time.sleep)
    MessageSender = SmsSender()


    def __init__(self, type):

        if 'Tongji' ==  type:
            self.MessageSender.set_app_info(top.appinfo('23476788', 'd7b403e513c48d1eebefb376050b8f85'))
            self.MessageSender.sms_type = "normal"
            self.MessageSender.rec_num = "13301856183"
            self.MessageSender.sms_free_sign_name = "同济信息中心"
            self.MessageSender.sms_template_code = "SMS_17400033"

    def checkTongjiInfo(self):
        response = urllib2.urlopen(SourceURL[0] + InfoCenterPostfix[0])
        html = response.read()
        #找到最新的一条消息
        pattern = u'''<div class="brief_info notice_ord">.*?<div class="date">(.*?)</div>.*?<div class="content">.*?<a href='../Notice/(.*?)'>.*?<span id="GridView1_lbTitle_0">(.*?)</span></a>'''
        Res = re.findall(pattern, html, re.S)[0]
        #看 最新的消息 和 保留的最新日期 以及 最后一个消息 和 保留的最后一个消息 是否一致
        if Res[0] != self.LastData and Res[2] != self.LastMessage:#不一致说明有新消息
            self.LastData = Res[0]      #更新最新的时间戳
            self.LastMessage = Res[2]   #更新最新的消息

            if len(self.LastMessage) > 24:
                substr = self.LastMessage[0:24] + "..."
            else:
                substr = self.LastMessage

            testlen = len(self.LastMessage)
            self.MessageSender.sms_param = "{\"name\" : \"" + substr + "\"}"
            res = self.MessageSender.getResponse()









    def timeLoop(self):
        CurrentTime = time.localtime(time.time())




test = InfoController('Tongji')

test.checkTongjiInfo()


