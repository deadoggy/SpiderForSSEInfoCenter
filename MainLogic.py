#coding:utf-8
import urllib2
import re
import time
import sched
import top.api.rest.AlibabaAliqinFcSmsNumSendRequest as SmsSender
import top
import top.api

SourceURL = ['http://sse.tongji.edu.cn']
InfoCenterPostfix = ['/InfoCenter/index.aspx']

class InfoController:
    LastData = ''
    LastMessage = ''
    schedule = sched.scheduler(time.time, time.sleep)
    MessageSender = SmsSender()
    LogFileName = 'log.txt'

    def __init__(self, type):

        if 'Tongji' ==  type:
            self.MessageSender.set_app_info(top.appinfo('23476788', 'd7b403e513c48d1eebefb376050b8f85'))
            self.MessageSender.sms_type = "normal"
            self.MessageSender.rec_num = "13301856183"
            self.MessageSender.sms_free_sign_name = "同济信息中心"
            self.MessageSender.sms_template_code = "SMS_17400033"

    def checkTongjiInfo(self):

        log = open(self.LogFileName, 'w+')
        response = {}
        try: #学院网有可能挂掉
            response = urllib2.urlopen(SourceURL[0] + InfoCenterPostfix[0])
        except Exception, e:
            log.write(e.message + "   " + str(time.localtime(time.time()))+ '\n')
            log.close()
            self.schedule.enter(60 * 60 * 4, 1, self.checkTongjiInfo, ())  # 每两个小时爬一次
            self.schedule.run()


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

            if res[u'alibaba_aliqin_fc_sms_num_send_response'][u'result'][u'success'] == True:
                log.write("Response[success] == True     Data:" + str(time.localtime(time.time()))+'\n')
            else:
                log.write("New Info but getReponse() sucks   Data:"  + str(time.localtime(time.time()))+'\n')
        else:
                log.write("No new info   Data:"  + str(time.localtime(time.time()))+'\n')
                log.wri

        log.close()
        self.schedule.enter( 60 * 60 *4, 1, self.checkTongjiInfo, ())#每两个小时爬一次
        self.schedule.run()






    def timeLoop(self):

        self.schedule.enter(0,1,self.checkTongjiInfo, ())
        self.schedule.run()







