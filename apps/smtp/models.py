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
    mail_user = models.CharField(verbose_name="用户名", max_length=50)
    mail_pass = models.CharField(verbose_name="授权口令", max_length=50)


    class Meta:
        verbose_name = "邮件服务器"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class EmailHeader(models.Model):
    name = models.CharField(verbose_name="名称", max_length=20, default="")
    from_name = models.CharField(verbose_name="发件人姓名", max_length=40, default="Phishing")
    from_addr = models.CharField(verbose_name="发件人地址", max_length=40)

    class Meta:
        verbose_name = "邮件头"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name