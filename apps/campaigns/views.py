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
from .forms import *
# 目标分组
from contacts.models import Group
# 邮件模板
from templets.models import Templet
# 钓鱼页面
from pages.models import Page
# 邮件服务器
from smtp.models import EmailServer
# 邮件头
from smtp.models import EmailHeader
from .task import *
########################################################################################################################
## 任务列表
########################################################################################################################
class CampaignListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'campaign_manage'
        web_func = 'campaign_list'
        campaigns = Campaign.objects.all()

        keywords = request.GET.get('keywords', '')

        if keywords != '':
            campaigns = campaigns.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords)
            )


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
            'campaigns': campaigns,
        }


        return render(request, 'campaigns/campaign_list.html', context=context)


########################################################################################################################
## 添加任务
########################################################################################################################
class AddCampaign(LoginRequiredMixin, View):
    def get(self, request):
        web_title = "campaign_manage"
        web_func = "campaign_add"

        groups = Group.objects.all()
        templets = Templet.objects.all()
        pages = Page.objects.all()
        servers = EmailServer.objects.all()
        headers = EmailHeader.objects.all()

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'groups': groups,
            'templets': templets,
            'pages': pages,
            'servers': servers,
            'headers': headers,
        }
        return render(request, 'campaigns/campaign_add.html', context=context)

########################################################################################################################
## 保存任务
########################################################################################################################
class SaveCampaign(LoginRequiredMixin, View):
    def post(self, request):
        add_campaign = AddCampaignForm(request.POST)
        if add_campaign != '':
            campaign = Campaign.objects.create(name=request.POST.get('name'))


            campaign.group = Group.objects.get(id=int(request.POST.get('group')))
            campaign.templet = Templet.objects.get(id=int(request.POST.get('templet')))
            campaign.page = Page.objects.get(id=int(request.POST.get('page')))

            server_list = request.POST.getlist('servers')
            #print(server_list)
            for i in server_list:
                print(i)
                campaign.servers.add(i)

            campaign.header = EmailHeader.objects.get(id=int(request.POST.get('header')))
            campaign.save()
            return HttpResponse('{"status":"success", "msg":"任务添加成功！"}', content_type='application/json')
        return HttpResponse('{"status":"fail", "msg":"任务内容不符合要求！"}', content_type='application/json')

########################################################################################################################
## 执行任务
########################################################################################################################
class ExecCampaign(LoginRequiredMixin, View):
    def post(self, request, ca_id):
        campaign = Campaign.objects.get(id=int(ca_id))

        try:
            task = post_email.delay(ca_id)
            # 改变任务状态
            campaign.status = 1
            campaign.save()
            return HttpResponse('{"status":"success", "msg":"开始执行"}', content_type='application/json')
        except:
            return HttpResponse('{"status":"failed", "msg":"执行失败"}', content_type='application/json')


########################################################################################################################
## 删除任务
########################################################################################################################
class DeleteCampaign(LoginRequiredMixin, View):
    def post(self, request, ca_id):
        try:
            campaign = Campaign.objects.get(id=int(ca_id))
            campaign.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')


########################################################################################################################
## 任务详情
########################################################################################################################
class CampaignDetail(LoginRequiredMixin, View):
    def get(self, request, ca_id):
        web_title = "campaign_manage"
        web_func = "campaign_detail"
        campaign = Campaign.objects.get(id=int(ca_id))

        task = caculate_time.delay(ca_id)
        context = {
            'web_title': web_title,
            'web_func': web_func,
            'campaign': campaign,
        }

        return render(request, "campaigns/campaign_detail.html", context=context)




