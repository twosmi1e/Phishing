#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 8:19 下午
# @Author  : twosmi1e
# @Site    : 
# @File    : forms.py
# @Software: PyCharm

from django import forms

from .models import *


class AddLinkmanForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    depart = forms.CharField(max_length=40, required=False)


class AddDepartForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)


class AddGroupForm(forms.Form):
    name = forms.CharField(max_length=20, required=True)
    group_members = forms.ModelMultipleChoiceField(queryset=Linkman.objects.all())