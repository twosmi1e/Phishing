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
import datetime

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *


########################################################################################################################
## 首页类视图
########################################################################################################################
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'page_manage'
        web_func = 'page_list'
        landing_pages = Page.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            landing_pages = landing_pages.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords) |
                Q(html__icontains=keywords) |
                Q(redirect_url__icontains=keywords)
            )

        else:
            display_chose = 'all'

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(landing_pages, 9, request=request)

        # 分页处理后的 QuerySet
        landing_pages = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'display_chose': display_chose,
            'pages': landing_pages,
        }
        return render(request, 'pages/page_list.html', context=context)


########################################################################################################################
## 添加页面
########################################################################################################################
class AddPage(LoginRequiredMixin, View):
    def post(self, request):
        add_page = AddPageForm(request.POST)
        if add_page.is_valid():
            page = Page()
            page.name = request.POST.get('name')
            page.html = request.POST.get('html')
            page.redirect_url = request.POST.get('redirect_url')
            if request.POST.get('capture_password'):
                page.capture_password = request.POST.get('capture_password')
            else:
                page.capture_password = False

            if request.POST.get('capture_username'):
                page.capture_username = request.POST.get('capture_username')
            else:
                page.capture_password = False

            page.save()
            return HttpResponse('{"status":"success", "msg":"添加页面成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加页面失败！"}', content_type='application/json')

########################################################################################################################
## 删除页面
########################################################################################################################
class DeletePage(LoginRequiredMixin, View):
    def post(self, request, p_id):
        try:
            page = Page.objects.get(id=int(p_id))
            page.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')

########################################################################################################################
## 页面详情
########################################################################################################################
class PageDetail(LoginRequiredMixin, View):
    def get(self, request, p_id):
        web_title = 'page_manage'
        web_func = 'page_detail'
        page = Page.objects.get(id=int(p_id))
        context = {
            'web_title': web_title,
            'wen_func': web_func,
            'page': page
        }
        return render(request, 'pages/page_detail.html', context=context)

########################################################################################################################
## 编辑页面
########################################################################################################################
class EditPage(LoginRequiredMixin, View):
    def post(self, request, p_id):
        page = Page.objects.get(id=int(p_id))
        #edit_templet_form = AddTempletForm(request.POST)
        edited_html = request.POST.get('html')
        if edited_html:
            page.html = edited_html
            page.save()
            return HttpResponse('{"status":"success", "msg":"修改页面成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改页面失败！"}', content_type='application/json')

