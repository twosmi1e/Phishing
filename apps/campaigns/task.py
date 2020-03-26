#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 15:23
# @Author  : twosmi1e
# @Site    : 
# @File    : task.py
# @Software: PyCharm

from __future__ import absolute_import
from celery import shared_task

from .models import *
from email.header import Header #处理邮件主题
from email.mime.text import MIMEText # 处理邮件内容
from email.utils import parseaddr, formataddr #用于构造特定格式的收发邮件地址
from Phishing.settings import WEB_URL
import smtplib
import time
import random

# 目标分组
from contacts.models import Group
# 邮件模板
from templets.models import Templet
# 钓鱼页面
from pages.models import Page
# 邮件服务器
from smtp.models import EmailServer
# 邮件头
from smtp.models import EmailHeader

#本地测试
CLICK_RECORD_URL = "http://127.0.0.1:8000/pages/click/"
#线上环境
#CLICK_RECORD_URL = WEB_URL+"pages/click/"

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 计算任务耗时
@shared_task()
def caculate_time(campaign_id):
    campaign = Campaign.objects.get(id=int(campaign_id))
    # 结束时间
    end_time = time.mktime(time.strptime(str(campaign.sendby_date), "%Y-%m-%d %H:%M:%S"))
    # 开始时间
    start_time = time.mktime(time.strptime(str(campaign.launch_date), "%Y-%m-%d %H:%M:%S"))
    campaign.complete_date = str(int(end_time)-int(start_time))
    campaign.save()


def choose_server(campaign):
    server_list = campaign.servers.get_queryset()
    length = len(server_list)
    # 随机取服务器
    i = random.randint(0, length-1)

    server_host = server_list[i].host
    server_port = server_list[i].port
    server_user = server_list[i].mail_user
    server_pass = server_list[i].mail_pass
    try:
        server = smtplib.SMTP(server_host, server_port)
        server.login(server_user, server_pass)
        print(server_list[i].name)
        return server, server_user
    except Exception as e:
        print(e)
        campaign.status = 3
        campaign.sendby_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        campaign.save()
        return False, False


@shared_task()
def post_email(campaign_id):
    # 获取任务对象
    campaign = Campaign.objects.get(id=int(campaign_id))

    # 任务开始时间
    campaign.launch_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


    # 获取邮件内容
    email_subject = campaign.templet.subject
    email_text = campaign.templet.text

    # 获取发送目标
    #target_name_list = campaign.group.get_name_list()
    #target_email_list = campaign.group.get_email_list()

    id_email_dict = campaign.group.get_id_email_dict()

    # 获取邮件头
    # 发信人名称
    from_name = campaign.header.from_name
   # print(from_name)
    from_addr = campaign.header.from_addr
   # print(from_addr)


    # 构造邮件内容
    for (id, email) in id_email_dict:
        to_addr = email
        url = CLICK_RECORD_URL+str(id)
        msg = MIMEText(email_text % (to_addr, url), 'HTML', 'utf-8')
        msg['To'] = _format_addr('<%s>' % to_addr)
        msg['From'] = _format_addr('%s<%s>' % (from_name, from_addr))
        msg['Subject'] = Header('%s' % email_subject, 'utf-8').encode()
        try:
            server, server_user = choose_server(campaign)
            if (server != False) and (server_user != False):
                print(server)
                print("login success")
            server.sendmail(server_user, to_addr, msg.as_string())
            # 降低发信频率 避免被拦截
            time.sleep(10)
            campaign.success_num = campaign.success_num+1
            print("send success")
        except smtplib.SMTPException as e:
            campaign.failed_num = campaign.failed_num+1
            print(e)

        # 修改任务状态
        campaign.status = 2
        # 任务结束时间
        campaign.sendby_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        campaign.save()
        print("mission complete!")














