from django.db import models



# Create your models here.
STATUS = (
     ('0','未开始'),
     ('1','执行中'),
     ('2','已完成'),
     ('3','执行错误'),
     )


class Campaign(models.Model):
    name = models.CharField(max_length=20, verbose_name="任务名称")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    launch_date = models.DateTimeField(null=True, verbose_name="开始时间")
    sendby_date = models.DateTimeField(null=True, verbose_name="结束时间")
    complete_date = models.CharField(blank=True, null=True, verbose_name="完成耗时", default="0", max_length=10)
    status = models.CharField(max_length=20, verbose_name="任务状态", choices=STATUS, default="0")

    group = models.ForeignKey('contacts.Group', verbose_name="分组", on_delete=models.DO_NOTHING, null=True, blank=True)
    templet = models.ForeignKey('templets.Templet', verbose_name="邮件模板", on_delete=models.DO_NOTHING, null=True, blank=True)
    page = models.ForeignKey('pages.Page', verbose_name="钓鱼页面", on_delete=models.DO_NOTHING, null=True, blank=True)
    servers = models.ManyToManyField('smtp.EmailServer', verbose_name="邮件服务器")
    header = models.ForeignKey('smtp.EmailHeader', verbose_name="邮件头", on_delete=models.DO_NOTHING, null=True, blank=True)

    # 任务结果数据统计
    success_num = models.IntegerField(blank=True, default=0, verbose_name="发送成功次数")
    failed_num = models.IntegerField(blank=True, default=0, verbose_name="发送失败次数")
    opened_num = models.IntegerField(blank=True, default=0, verbose_name="已读邮件数")

    class Meta:
        verbose_name = "发送任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_servers(self):
        return "\n".join([s.name for s in self.servers.all()])


