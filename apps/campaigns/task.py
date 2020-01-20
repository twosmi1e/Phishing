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

@shared_task()
def PostEmail(campaign_id):
    campaign = Campaign.objects.get(id=int(campaign_id))
