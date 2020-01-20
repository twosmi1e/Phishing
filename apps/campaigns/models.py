from django.db import models



# Create your models here.
STATUS=(
     ('0','未开始'),
     ('1','执行中'),
     ('2','已完成'),
     ('3','已结束'),
     )


class Campaign(models.Model):
    name = models.CharField(max_length=20, verbose_name="任务名称")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建时间")
    launch_date = models.DateField(blank=True, verbose_name="开始时间")
    sendby_date = models.DateField(blank=True, verbose_name="结束时间")
    complete_date = models.DateField(blank=True, null=True, verbose_name="完成时间")
    status = models.CharField(max_length=20, verbose_name="任务状态", choices=STATUS, default="0")

    group = models.ForeignKey('contacts.Group', verbose_name="分组", on_delete=models.DO_NOTHING)
    templet = models.ForeignKey('templets.Templet', verbose_name="邮件模板", on_delete=models.DO_NOTHING, default="")
    page = models.ForeignKey('pages.Page', verbose_name="钓鱼页面", on_delete=models.DO_NOTHING)
    server = models.ForeignKey('smtp.EmailServer', verbose_name="邮件服务器", on_delete=models.DO_NOTHING)
    header = models.ForeignKey('smtp.EmailHeader', verbose_name="邮件头", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "发送任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


