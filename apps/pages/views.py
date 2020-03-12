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
from .task import *
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
                Q(redirect_url__icontains=keywords)
            )



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
            page.redirect_url = request.POST.get('redirect_url')
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
## 编辑页面
########################################################################################################################
class EditPage(LoginRequiredMixin, View):
    def post(self, request, p_id):
        edit_page = AddPageForm(request.POST)
        if edit_page.is_valid():
            page = Page.objects.get(id=int(p_id))
            page.name = request.POST.get('name')
            page.redirect_url = request.POST.get('redirect_url')
            page.save()
            return HttpResponse('{"status":"success", "msg":"编辑页面成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"编辑页面失败！"}', content_type='application/json')


########################################################################################################################
## 切换页面
########################################################################################################################
class SelectPage(LoginRequiredMixin, View):
    def post(self, request, p_id):
        global select_page_id
        select_page_id = p_id
        if select_page_id:
            return HttpResponse('{"status":"success", "msg":"切换页面成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"切换页面失败！"}', content_type='application/json')


########################################################################################################################
## 点击记录
########################################################################################################################
class ClickRecord(View):
    def get(self, request, v_id):
        global select_page_id
        agent = request.META['HTTP_USER_AGENT']
        ip = request.META['REMOTE_ADDR']

        task = add_record.delay(agent, ip, v_id)
        # 获取跳转链接
        page = Page.objects.get(id=int(select_page_id))
        redirect_url = page.redirect_url

        context = {
            'r_url': redirect_url,
        }
        return render(request, "pages/page_for_phishing.html", context=context)




