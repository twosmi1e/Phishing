#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 16:42
# @Author  : twosmi1e
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms
from .models import *

class AddServerForm(forms.ModelForm):
    class Meta:
        model = EmailServer