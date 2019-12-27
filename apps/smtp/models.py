from django.db import models

# Create your models here.


class EmailServer(models.Model):
    INTERFACE_TYPE = (
        ('1', 'POP3'),
        ('2', 'SMTP'),
        ('3', 'IMAP'),
    )
    name = models.CharField(verbose_name="服务器名称", max_length=20)
    interface = models.CharField(verbose_name="服务器类型", choices=INTERFACE_TYPE, max_length=10)
    host = models.CharField(verbose_name="服务器地址", max_length=40)
    port = models.CharField(verbose_name="端口", default="25", max_length=10)
    mail_user = models.CharField(verbose_name="用户名", max_length=20)
    mail_pass = models.CharField(verbose_name="授权口令", max_length=20)

    class Meta:
        verbose_name = "邮件服务器"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class EmailHeader(models.Model):
    from_addr = models.CharField(verbose_name="发件人", max_length=40)
    to_addr = models.CharField(verbose_name="收件人", max_length=40)

    class Meta:
        verbose_name = "邮件头"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name