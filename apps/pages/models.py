from django.db import models

# Create your models here.



class Page(models.Model):
    name = models.CharField(verbose_name="页面名称", max_length=20)
    redirect_url = models.URLField(verbose_name="跳转链接", blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "钓鱼页面"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ClickRecord(models.Model):
    victim = models.ForeignKey('contacts.Linkman', verbose_name="点击者", on_delete=models.DO_NOTHING)
    agent = models.CharField(verbose_name="客户端", max_length=200, blank=True, null=True)
    ip = models.GenericIPAddressField(verbose_name="点击者IP", blank=True, null=True)
    add_time = models.DateTimeField(verbose_name="点击时间", auto_now_add=True)

    class Meta:
        verbose_name = "点击记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
