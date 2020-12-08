from django.db import models


# Create your models here.


class Templet(models.Model):
    name = models.CharField(max_length=20, verbose_name="模板名称")
    subject = models.CharField(max_length=40, verbose_name="邮件标题")
    text = models.TextField(verbose_name="邮件内容")
    attachments = models.FileField(upload_to="attach/%Y/%M", blank=True, verbose_name="附件")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "邮件模板"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

