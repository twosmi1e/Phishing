#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 11:17
# @Author  : twosmi1e
# @Site    : 
# @File    : task.py
# @Software: PyCharm

from __future__ import absolute_import
from celery import shared_task

from .models import *
from .utils import *


# 遍历查找需要的部门json
def get_dep_by_name(name):
    dti = DingTalkInterface()
    scope = dti.get_scope()
    # 所有部门名称
    for id in scope:
        departments = dti.get_department_list(id)
        for dep in departments:
            #print(dep["name"])
            if dep["name"] == name:
                result = dep
                return result

    return None

# 根据钉钉部门id获取部门人员信息并导入存储
def get_user_by_dept(dt_dept_id, sys_dept_id):
    dti = DingTalkInterface()
    userid_list = dti.get_userid_list(dt_dept_id)

    for id in userid_list:
        user_detail = dti.get_user_detail(id)
        print(user_detail["name"], user_detail["email"])
        try:
            if Linkman.objects.filter(name=user_detail["name"]):
                print("已有此员工信息")
            else:
                linkman = Linkman()
                linkman.name = user_detail["name"]
                linkman.email = user_detail["email"]
                linkman.depart_id = sys_dept_id
                linkman.save()
                print("添加成功")

        except Exception as e:
            print(e)



# 获取指定部门下人员信息并全部导入
@shared_task()
def get_dept_user(dep):
    #count = 0  # 计数导入人数
    #failed = 0  # 导入失败人数

    dti = DingTalkInterface()
    # 提取json中信息
    dt_dept_id = dep["id"]
    dept_name = dep["name"]

    if Department.objects.filter(name=dept_name):
        sys_dept = Department.objects.get(name=dept_name)
        # 获取部门人员
        get_user_by_dept(dt_dept_id, sys_dept.id)
    else:
        department = Department.objects.create(name=dept_name)
        get_user_by_dept(dt_dept_id, department.id)

    # 获取所有子部门
    all_dept_list = dti.get_department_list(dt_dept_id)
    for dept in all_dept_list:
        print(dept["name"])
        # 根据结果添加部门
        if Department.objects.filter(name=dept["name"]):
            print("已导入过此部门")
            sys_dept_2 = Department.objects.get(name=dept_name)
            get_user_by_dept(dept["id"], sys_dept_2.id)
        else:
            department = Department.objects.create(name=dept["name"])
            get_user_by_dept(dept["id"], department.id)







