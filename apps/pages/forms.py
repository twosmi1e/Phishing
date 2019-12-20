#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 09:54
# @Author  : twosmi1e
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from .models import *


class AddPageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ['add_time']