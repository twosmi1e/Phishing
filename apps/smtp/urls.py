#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 16:42
# @Author  : twosmi1e
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.urls import path


########################################################################################################################
## 系统自带模块导入
########################################################################################################################
from .views import *
########################################################################################################################
## 自建模块导入
########################################################################################################################


########################################################################################################################
## url
########################################################################################################################
app_name = 'smtp'

urlpatterns = [
    # 服务器配置
    path('server/list/', ServerListView.as_view(), name='server_list'),
    # 添加配置
    path('server/add', AddServer.as_view(), name='add_server'),
    # 发送测试邮件
    path('server/sendmail', SendTestEmail.as_view(), name='send_test_email'),
    # 删除配置
    path('server/del/<int:s_id>', DeleteServer.as_view(), name='del_server'),
    # 编辑配置
    path('server/edit/<int:s_id>', EditServer.as_view(), name='edit_server'),
    # 邮件头列表
    path('header/list/', HeaderListView.as_view(), name='header_list'),
    # 添加邮件头
    path('header/add', AddHeader.as_view(), name='add_header'),
    # 删除邮件头
    path('header/del/<int:h_id>', DeleteHeader.as_view(), name='del_header'),
    # 编辑邮件头
    path('header/edit/<int:h_id>', EditHeader.as_view(), name='edit_header'),
    # 邮件头测试
    path('header/test/<int:h_id>', TestHeader.as_view(), name='test_header'),
]
