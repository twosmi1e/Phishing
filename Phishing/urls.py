"""Phishing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # 用户url入口
    path('', include('users.urls', namespace='users')),
    # 验证码
    path('captcha/', include('captcha.urls')),
    # 联系人
    path('contacts/', include('contacts.urls', namespace='contacts')),
    # 邮件模板
    path('templets/', include('templets.urls', namespace='templets')),
    # 钓鱼页面
    path('pages/', include('pages.urls', namespace='pages')),
]
