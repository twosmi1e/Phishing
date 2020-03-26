from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
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
from email.utils import parseaddr, formataddr #用于构造特定格式的收发邮件地址
import smtplib #用于发送邮件
import json
########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *


########################################################################################################################
## 列表类视图
########################################################################################################################
class ServerListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'server_manage'
        web_func = 'server_list'
        email_server = EmailServer.objects.all()
        interface_choice = EmailServer.INTERFACE_TYPE
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            email_server = email_server.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords) |
                Q(host__icontains=keywords)
            )


        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(email_server, 9, request=request)

        # 分页处理后的 QuerySet
        email_server = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'emailservers': email_server,
            'interface_choice': interface_choice,
        }
        return render(request, 'smtpconfig/server_list.html', context=context)

########################################################################################################################
## 添加配置
########################################################################################################################
class AddServer(LoginRequiredMixin, View):
    def post(self, request):
        add_server = AddServerForm(request.POST)
        if add_server.is_valid():
            server = EmailServer()
            server.name = request.POST.get('name')
            server.interface = request.POST.get('interface')
            server.host = request.POST.get('host')
            server.port = request.POST.get('port')
            server.mail_user = request.POST.get('mail_user')
            server.mail_pass = request.POST.get('mail_pass')
            server.save()
            return HttpResponse('{"status":"success", "msg":"添加服务器成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加服务器失败！"}', content_type='application/json')

########################################################################################################################
## 邮件发送测试
########################################################################################################################
class SendTestEmail(LoginRequiredMixin, View):
    # 格式化邮件头
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def post(self, request):
        server_host = request.POST.get('host')
        server_port = request.POST.get('port')
        server_mail_user = request.POST.get('mail_user')
        server_mail_pass = request.POST.get('mail_pass')

        to_addr = request.POST.get('to_addr')

        # 登录邮件服务器
        try:
            server = smtplib.SMTP(server_host, server_port)
            server.login(server_mail_user, server_mail_pass)
        except:
            return HttpResponse('{"status":"fail", "msg":"无法连接邮件服务器！"}', content_type='application/json')
        # 构造测试邮件
        msg = MIMEText('邮件服务器配置有效!', 'plain', 'utf-8')
        msg['To'] = self._format_addr('<%s>' % to_addr)
        msg['From'] = self._format_addr('Phishing<%s>' % server_mail_user)
        msg['Subject'] = Header('邮件发送测试', 'utf-8').encode()
        try:
            server.sendmail(server_mail_user, to_addr, msg.as_string())
            return HttpResponse('{"status":"success", "msg":"发送成功！"}', content_type='application/json')
        except:
            return HttpResponse('{"status":"fail", "msg":"发送失败！"}', content_type='application/json')


########################################################################################################################
## 删除配置
########################################################################################################################
class DeleteServer(LoginRequiredMixin, View):
    def post(self, request, s_id):
        try:
            server = EmailServer.objects.get(id=int(s_id))
            server.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')

########################################################################################################################
## 编辑配置
########################################################################################################################
class EditServer(LoginRequiredMixin, View):
    def post(self, request, s_id):
        server = EmailServer.objects.get(id=int(s_id))
        edit_server = AddServerForm(request.POST)
        if edit_server.is_valid():
            server.name = request.POST.get('name')
            server.interface = request.POST.get('interface')
            server.host = request.POST.get('host')
            server.port = request.POST.get('port')
            server.mail_user = request.POST.get('mail_user')
            server.mail_pass = request.POST.get('mail_pass')
            server.save()
            return HttpResponse('{"status":"success", "msg":"编辑成功!"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"编辑失败!"}', content_type='application/json')

########################################################################################################################
## 邮件头列表
########################################################################################################################
class HeaderListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'header_manage'
        web_func = 'header_list'
        email_header = EmailHeader.objects.all()
        email_server = EmailServer.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            email_header = email_header.filter(
                Q(id__icontains=keywords) |
                Q(name__icontains=keywords) |
                Q(from_name__icontains=keywords)
            )

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(email_header, 9, request=request)

        # 分页处理后的 QuerySet
        email_header = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'emailheaders': email_header,
            'emailservers': email_server,
        }
        return render(request, 'smtpconfig/header_list.html', context=context)

########################################################################################################################
## 添加邮件头
########################################################################################################################
class AddHeader(LoginRequiredMixin, View):
    def post(self, request):
        add_header = AddHeaderForm(request.POST)
        if add_header.is_valid():
            header = EmailHeader()
            header.name = request.POST.get('name')
            header.from_name = request.POST.get('from_name')
            header.from_addr = request.POST.get('from_addr')
            header.save()
            return HttpResponse('{"status":"success", "msg":"添加邮件头成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加邮件头失败！"}', content_type='application/json')

########################################################################################################################
## 删除邮件头
########################################################################################################################
class DeleteHeader(LoginRequiredMixin, View):
    def post(self, request, h_id):
        try:
            header = EmailHeader.objects.get(id=int(h_id))
            header.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')


########################################################################################################################
## 编辑邮件头
########################################################################################################################
class EditHeader(LoginRequiredMixin, View):
    def post(self, request, h_id):
        header = EmailHeader.objects.get(id=int(h_id))
        edit_header = AddHeaderForm(request.POST)
        if edit_header.is_valid():
            header.name = request.POST.get('name')
            header.from_name = request.POST.get('from_name')
            header.from_addr = request.POST.get('from_addr')
            header.save()
            return HttpResponse('{"status":"success", "msg":"编辑成功!"}', content_type='application/json')

        return HttpResponse('{"status":"fail", "msg":"编辑失败!"}', content_type='application/json')

########################################################################################################################
## 测试邮件头
########################################################################################################################
class TestHeader(LoginRequiredMixin, View):
    # 格式化邮件头
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def post(self, request, h_id):
        eheader = EmailHeader.objects.get(id=int(h_id))
        server_id = request.POST.get('server')
        eserver = EmailServer.objects.get(id=int(server_id))
        to_addr = request.POST.get('to_addr')

        # 登录邮件服务器
        try:
            server = smtplib.SMTP(eserver.host, eserver.port)
            server.login(eserver.mail_user, eserver.mail_pass)
        except:
            return HttpResponse('{"status":"fail", "msg":"无法连接邮件服务器！"}', content_type='application/json')
        # 构造测试邮件
        msg = MIMEText('邮件服务器配置有效!请检查邮件头!', 'plain', 'utf-8')
        msg['To'] = self._format_addr('<%s>' % to_addr)
        msg['From'] = self._format_addr('%s<%s>' % (eheader.from_name, eheader.from_addr))
        msg['Subject'] = Header('邮件发送测试', 'utf-8').encode()
        try:
            server.sendmail(eserver.mail_user, to_addr, msg.as_string())
            return HttpResponse('{"status":"success", "msg":"发送成功！"}', content_type='application/json')
        except smtplib.SMTPException as e:
            msg = str(e)
            data = {
                'status': 'fail',
                'msg': msg
            }
            return JsonResponse(data)

