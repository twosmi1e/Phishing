from django.shortcuts import render

# Create your views here.
########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import json
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *


########################################################################################################################
## 联系人列表视图
########################################################################################################################
class LinkmanListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'linkman_manage'
        web_func = 'linkman_list'
        all_linkman = Linkman.objects.all()
        departments = Department.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            all_linkman = all_linkman.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords) |
                Q(email__icontains=keywords) |
                Q(depart__name__icontains=keywords)
            )

        else:
            display_chose = 'all'

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(all_linkman, 9, request=request)

        # 分页处理后的 QuerySet
        all_linkman = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'all_linkman': all_linkman,
            'display_chose': display_chose,
            'departments': departments,
        }
        return render(request, 'contacts/linkman_list.html', context=context)

########################################################################################################################
## 添加联系人
########################################################################################################################
class AddLinkman(LoginRequiredMixin, View):
    def post(self, request):
        add_linkman_host = AddLinkmanForm(request.POST)
        if add_linkman_host.is_valid():
            if Linkman.objects.filter(email=request.POST.get('email')):
                return HttpResponse('{"status":"fail", "msg":"记录已存在！"}', content_type='application/json')
            linkman = Linkman()
            linkman.name = request.POST.get('name')
            linkman.email = request.POST.get('email')
            linkman.depart_id = request.POST.get('depart')
            linkman.save()
            return HttpResponse('{"status":"success", "msg":"记录添加成功！"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"内容不符合要求！"}', content_type='application/json')


########################################################################################################################
## 编辑联系人
########################################################################################################################
class EditLinkman(LoginRequiredMixin, View):
    def post(self, request, l_id):
        old_record = Linkman.objects.get(id=int(l_id))
        edit_linkman_form = AddLinkmanForm(request.POST)
        if edit_linkman_form.is_valid():

            linkman = Linkman()
            linkman.id = old_record.id
            old_record.delete()
            linkman.name = request.POST.get('name')
            linkman.email = request.POST.get('email')
            linkman.depart_id = request.POST.get('depart')
            linkman.save()
            return HttpResponse('{"status:"success", "mag":"编辑成功!" "}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"修改失败！"}', content_type='application/json')

########################################################################################################################
## 部门列表视图
########################################################################################################################
class DepartListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'depart_manage'
        web_func = 'depart_list'
        departments = Department.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            departments = departments.filter(
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
        p = Paginator(departments, 9, request=request)

        # 分页处理后的 QuerySet
        departments = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'display_chose': display_chose,
            'departments': departments,
        }
        return render(request, 'contacts/depart_list.html', context=context)


########################################################################################################################
## 添加部门
########################################################################################################################
class AddDepart(LoginRequiredMixin, View):
    def post(self, request):
        add_depart = AddDepartForm(request.POST)
        if add_depart.is_valid():
            if Department.objects.filter(name=request.POST.get('name')):
                return HttpResponse('{"status":"fail", "msg":"部门已存在！"}', content_type='application/json')
            depart = Department()
            depart.name = request.POST.get('name')

            depart.save()
            return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"内容不符合要求！"}', content_type='application/json')


########################################################################################################################
## 分组列表
########################################################################################################################
class GroupListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'group_manage'
        web_func = 'group_list'
        groups = Group.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            groups = groups.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords) |
                Q(group_members__name__icontains=keywords)
            )

        else:
            display_chose = 'all'

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(groups, 9, request=request)

        # 分页处理后的 QuerySet
        groups = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'display_chose': display_chose,
            'groups': groups,
        }
        return render(request, 'contacts/group_list.html', context=context)