from django.db import models

# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=20, verbose_name="任务名称")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建时间")
    launch_date = models.DateField(auto_now_add=True, verbose_name="开始时间")
    sendby_date = models.DateField(blank=True, verbose_name="结束时间")
    complete_date = models.DateField(verbose_name="完成时间")

    group = models
