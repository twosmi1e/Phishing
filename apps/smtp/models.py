from django.db import models

# Create your models here.

class EmailServer(models.Model):
    INTERFACE_TYPE = (
        ('1', 'POP3'),
        ('2', 'SMTP'),
        ('3', 'IMAP'),
    )
    name = models.CharField(verbose_name="服务器名称", max_length=20)
    interface = models.CharField(verbose_name="服务器类型", choices=INTERFACE_TYPE)
    host = models.CharField(verbose_name="服务器地址")
    port = models.CharField(verbose_name="端口", default="25")
    mail_user = models.CharField(verbose_name="用户名")
    mail_pass = models.CharField(verbose_name="授权口令")

class EmailHeader(models.Model):
    from_addr = models.CharField(verbose_name="发件人")
    to_addr = models.CharField(verbose_name="收件人")