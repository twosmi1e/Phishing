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
import smtplib
import time

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

@shared_task()
def post_email(campaign_id):
    # 获取任务对象
    campaign = Campaign.objects.get(id=int(campaign_id))


    # 任务开始时间
    campaign.launch_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 获取邮件服务器
    server_host = campaign.server.host

    server_port = campaign.server.port

    server_user = campaign.server.mail_user

    server_pass = campaign.server.mail_pass


    # 获取邮件内容
    email_subject = campaign.templet.subject
    email_text = campaign.templet.text
    #print(email_text)
    # 获取发送目标
    target_name_list = campaign.group.get_name_list()
    target_email_list = campaign.group.get_email_list()
    #print(target_name_list)
    #print(target_email_list)
    # 获取邮件头
    # 发信人名称
    from_name = campaign.header.from_name
   # print(from_name)
    from_addr = campaign.header.from_addr
   # print(from_addr)

    # 登录邮件服务器
    try:
        server = smtplib.SMTP(server_host, server_port)
        server.login(server_user, server_pass)
    except:
        print("login failed")


    # 构造邮件内容
    for email in target_email_list:
        to_addr = email
        msg = MIMEText(email_text % to_addr, 'HTML', 'utf-8')
        msg['To'] = _format_addr('<%s>' % to_addr)
        msg['From'] = _format_addr('%s<%s>' % (from_name, from_addr))
        msg['Subject'] = Header('%s' % email_subject, 'utf-8').encode()
        try:
            server.sendmail(server_user, to_addr, msg.as_string())
            # 降低发信频率 避免被拦截
            time.sleep(3)
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














