#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/17 14:29
# @Author  : twosmi1e
# @Site    : 
# @File    : task.py
# @Software: PyCharm

from __future__ import absolute_import
from celery import shared_task

from .models import *
from contacts.models import Linkman

@shared_task()
def add_record(agent, ip, v_id):
    record = ClickRecord()
    record.victim = Linkman.objects.get(id=int(v_id))
    record.agent = agent
    record.ip = ip
    record.save()