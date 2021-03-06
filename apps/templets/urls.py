#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 19:54
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
app_name = 'templets'

urlpatterns = [
    # 列表视图
    path('list', IndexView.as_view(), name='templet_list'),
    # 添加模板
    path('add', AddTemplet.as_view(), name='add_templet'),
    # 删除模板
    path('del/<int:t_id>', DeleteTemplet.as_view(), name='del_templet'),
    # 编辑模板
    path('edit/<int:t_id>', EditTemplet.as_view(), name='edit_templet'),
    # 模板详情
    path('detail/<int:t_id>', TempletDetail.as_view(), name='templet_detail'),
]


