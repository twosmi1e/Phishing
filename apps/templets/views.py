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
from utils.sendmail_utils import *
from utils.other_func import *


########################################################################################################################
## 首页类视图
########################################################################################################################
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'templet_manage'
        web_func = 'templet_list'
        templet = Templet.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            templet = templet.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords) |
                Q(subject__icontains=keywords)
            )

        else:
            display_chose = 'all'

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(templet, 9, request=request)

        # 分页处理后的 QuerySet
        templet = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'display_chose': display_chose,
            'templets': templet,
        }
        return render(request, 'templets/templet_list.html', context=context)

########################################################################################################################
## 添加模板
########################################################################################################################
class AddTemplet(LoginRequiredMixin, View):
    def post(self, request):
        add_templet = AddTempletForm(request.POST)
        if add_templet.is_valid():
            templet = Templet()
            templet.name = request.POST.get('name')
            templet.subject = request.POST.get('subject')
            templet.text = request.POST.get('text')
            templet.save()
            return HttpResponse('{"status":"success", "msg":"添加模板成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加模板失败！"}', content_type='application/json')


########################################################################################################################
## CKEDITOR 上传图片
########################################################################################################################
@csrf_protect
def upload_image(request):
    if request.method == 'POST':
        callback = request.GET.get('CKEditorFuncNum')
        try:
            # path 修改上传的路径
            path = "upload/ckeditor/image/" + time.strftime("%Y%m%d%H%M%S",time.localtime())
            f = request.FILES["upload"]
            file_name = path + "_" + f.name
            des_origin_f = open(file_name, "wb+")
            # 直接遍历类文件类型就可以生成迭代器了
            for chunk in f:
                des_origin_f.write(chunk)
            des_origin_f.close()
        except Exception as e:
            print(e)
        res = r"<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'/"+file_name+"', '');</script>"
        return HttpResponse(res)
    else:
        raise Http404()

########################################################################################################################
## 删除模板
########################################################################################################################
class DeleteTemplet(LoginRequiredMixin, View):
    def post(self, request, t_id):
        try:
            templet = Templet.objects.get(id=int(t_id))
            templet.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')


########################################################################################################################
## 编辑模板
########################################################################################################################
class EditTemplet(LoginRequiredMixin, View):
    def post(self, request, t_id):
        old_templet = Templet.objects.get(id=int(t_id))
        edit_templet_form = AddTempletForm(request.POST)
        if edit_templet_form.is_valid():
            templet = Templet()
            templet.id = old_templet.id
            old_templet.delete()
            templet.name = request.POST.get('name')
            templet.subject = request.POST.get('subject')
            templet.text = request.POST.get('text')
            templet.save()
            return HttpResponse('{"status":"success", "msg":"修改模板成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改模板失败！"}', content_type='application/json')
