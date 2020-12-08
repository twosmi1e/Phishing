from django.shortcuts import render

# Create your views here.
########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.http import HttpResponse
from django.db.models import Q

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import json
import xlrd
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *
from .task import *

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

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(all_linkman, 12, request=request)

        # 分页处理后的 QuerySet
        all_linkman = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'all_linkman': all_linkman,
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
        linkman = Linkman.objects.get(id=int(l_id))
        edit_linkman_form = AddLinkmanForm(request.POST)
        if edit_linkman_form.is_valid():
            linkman.name = request.POST.get('name')
            linkman.email = request.POST.get('email')
            linkman.depart_id = request.POST.get('depart')
            linkman.save()
            return HttpResponse('{"status":"success", "msg":"编辑成功!"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"修改失败!"}', content_type='application/json')


########################################################################################################################
## 删除联系人
########################################################################################################################
class DeleteLinkman(LoginRequiredMixin, View):
    def post(self, request, l_id):
        try:
            linkman = Linkman.objects.get(id=int(l_id))
            linkman.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')

########################################################################################################################
## 部门列表视图
########################################################################################################################
class DepartListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'depart_manage'
        web_func = 'depart_list'
        departments = Department.objects.all()
        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            departments = departments.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords)
            )


        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(departments, 12, request=request)

        # 分页处理后的 QuerySet
        departments = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
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
## 编辑部门
########################################################################################################################
class EditDepart(LoginRequiredMixin, View):
    def post(self, request, d_id):
        depart = Department.objects.get(id=int(d_id))
        edit_depart_form = AddDepartForm(request.POST)
        if edit_depart_form.is_valid():
            depart.name = request.POST.get('name')
            depart.save()
            return HttpResponse('{"status":"success", "msg":"编辑成功!"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"修改失败!"}', content_type='application/json')

########################################################################################################################
## 删除部门
########################################################################################################################
class DeleteDepart(LoginRequiredMixin, View):
    def post(self, request, d_id):
        try:
            depart = Department.objects.get(id=int(d_id))
            depart.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')

########################################################################################################################
## 分组列表
########################################################################################################################
class GroupListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'group_manage'
        web_func = 'group_list'
        groups = Group.objects.all()
        linkmen = Linkman.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            groups = groups.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords) |
                Q(group_members__name__icontains=keywords)
            )

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
            'groups': groups,
            'linkmen': linkmen,
        }
        return render(request, 'contacts/group_list.html', context=context)

########################################################################################################################
## 添加分组
########################################################################################################################
class AddGroup(LoginRequiredMixin, View):
    def post(self, request):
        add_group = AddGroupForm(request.POST)
        if add_group != '':
            if Group.objects.filter(name=request.POST.get('name')):
                return HttpResponse('{"status":"fail", "msg":"分组已存在！"}', content_type='application/json')
            group = Group.objects.create(name=request.POST.get('name'))
            members = request.POST.getlist('members[]')
            num = len(members)

            for i in range(num):
                group.group_members.add(members[i])

            return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"内容不符合要求！"}', content_type='application/json')

########################################################################################################################
## 删除分组
########################################################################################################################
class DeleteGroup(LoginRequiredMixin, View):
    def post(self, request, g_id):
        try:
            group = Group.objects.get(id=int(g_id))
            group.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')

########################################################################################################################
## 分组详情
########################################################################################################################
class GroupDetail(LoginRequiredMixin, View):
    def get(self, request, g_id):
        web_title = 'group_manage'
        web_func = 'group_detail'
        group = Group.objects.get(id=int(g_id))

        id_list = Group.get_id_list(group)
        member_list = []
        for id in id_list:
            linkman = Linkman.objects.get(id=int(id))
            member_list.append(linkman)
        context = {
            'web_title': web_title,
            'web_func': web_func,
            'group': group,
            'members': member_list,
        }
        return render(request, 'contacts/group_detail.html', context=context)


########################################################################################################################
## 批量添加
########################################################################################################################
class BatchImport(LoginRequiredMixin, View):
    def post(self, request):
        dep_name = request.POST.get('dep_name')
        group_name = request.POST.get('group_name')
        print(group_name)
        department = get_dep_by_name(dep_name)
        print(department)
        if department == None:
            return HttpResponse('{"status":"fail", "msg":"无此部门！"}', content_type='application/json')
        else:
            if group_name:
                task = get_user_create_group.delay(department, group_name)
                return HttpResponse('{"status":"success", "msg":"开始导入并分组！"}', content_type='application/json')
            else:
                task = get_dept_user.delay(department)
                return HttpResponse('{"status":"success", "msg":"开始导入！"}', content_type='application/json')


########################################################################################################################
## 上传excel
########################################################################################################################

