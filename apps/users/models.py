########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


########################################################################################################################
## 系统自带模块导入
########################################################################################################################


########################################################################################################################
## 自建模块导入
########################################################################################################################



########################################################################################################################
## 用户模块
########################################################################################################################
class UserProfile(AbstractUser):
    name = models.CharField(verbose_name='姓名', max_length=20)
    role = models.CharField(verbose_name='用户角色', max_length=20)
    avatar = models.ImageField(verbose_name='用户头像', max_length=200, upload_to='users/avatar/%Y/%m',
                               default='users/avatar/default.png', null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username




########################################################################################################################
## 邮箱验证码
########################################################################################################################
class EmailVerificationCode(models.Model):
    code = models.CharField(verbose_name='验证码', max_length=20)
    email = models.EmailField(verbose_name='接收邮箱')
    use = models.CharField(verbose_name='用途',
                           choices=(('register', '注册'), ('forget', '忘记密码'), ('change_email', '修改邮箱')), max_length=20)
    is_use = models.BooleanField(verbose_name='是否使用', default=False)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


########################################################################################################################
## 用户登录信息表
########################################################################################################################
class UserLoginRecord(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    agent = models.CharField(verbose_name='客户端', max_length=200, blank=True, null=True)
    ip = models.GenericIPAddressField(verbose_name='客户端IP', blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户登录信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username




















