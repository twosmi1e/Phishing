#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 16:45
# @Author  : twosmi1e
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms

from .models import *


class AddCampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = []
