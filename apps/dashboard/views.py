from django.shortcuts import render

# Create your views here.

########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.http import HttpResponse
from django.db.models import Count, Sum
########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import json
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

########################################################################################################################
## 自建模块导入
########################################################################################################################
from contacts.models import Linkman
from campaigns.models import Campaign
from pages.models import ClickRecord
from utils.mixin_utils import *

########################################################################################################################
## 首页视图
########################################################################################################################
class IndexView(View):
    def get(self, request):
        web_title = "dashboard"
        web_func = "dashboard"

        # 获取目标数量
        number_of_linkman = Linkman.objects.count()
        # 获取任务数量
        number_of_campaign = Campaign.objects.count()

        success_email = Campaign.objects.all().aggregate(number=Sum('success_num'))
        failed_email = Campaign.objects.all().aggregate(number=Sum('failed_num'))

        clickrecord = ClickRecord.objects.count()

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'linkman': number_of_linkman,
            'campaign': number_of_campaign,
            'success': success_email['number'],
            'failed': failed_email['number'],
            'clickrecord': clickrecord
        }


        return render(request, "dashboard/index.html", context=context)

########################################################################################################################
## 点击记录表
########################################################################################################################
class ClickRecordView(View):
    def get(self, request):
        web_title = 'dashboard'
        web_func = 'login_record'
        all_records = ClickRecord.objects.all().order_by('-add_time')

        keywords = request.GET.get('keywords', '')

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(all_records, 15, request=request)

        # 分页处理后的 QuerySet
        all_records = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'all_records': all_records,
        }
        return render(request, 'dashboard/click_record.html', context=context)