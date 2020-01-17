from django.shortcuts import render

# Create your views here.
########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import time
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
from email.header import Header #处理邮件主题
from email.mime.text import MIMEText # 处理邮件内容



########################################################################################################################
## 自建模块导入
########################################################################################################################

from .models import *
from utils.mixin_utils import *


########################################################################################################################
## 任务列表
########################################################################################################################
class CampaignListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'campaign_manage'
        web_func = 'campaign_ist'
        campaigns = Campaign.objects.all()

        keywords = request.GET.get('keywords', '')

        if keywords != '':
            campaigns = campaigns.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords)
            )

        else:
            display_chose = 'all'

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(campaigns, 9, request=request)

        # 分页处理后的 QuerySet
        campaigns = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'display_chose': display_chose,
            'campaigns': campaigns,
        }
        return render(request, 'campaigns/campaign_list.html', context=context)


########################################################################################################################
## 添加任务
########################################################################################################################
class AddCampaign(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'campaigns/campaign_add.html')


