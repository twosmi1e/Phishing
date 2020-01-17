#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 15:23
# @Author  : twosmi1e
# @Site    : 
# @File    : task.py
# @Software: PyCharm

from __future__ import absolute_import
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y
