#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 19:44
# @Author  : twosmi1e
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from .models import *


class AddTempletForm(forms.ModelForm):
    class Meta:
        model = Templet
        exclude = ['add_time']
