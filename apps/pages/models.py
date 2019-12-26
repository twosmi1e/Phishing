from django.db import models

# Create your models here.


########################################################################################################################
## 钓鱼页面
########################################################################################################################


class Page(models.Model):
    name = models.CharField(verbose_name="页面名称", max_length=20)
    html = models.TextField(verbose_name="页面代码")
    redirect_url = models.URLField(verbose_name="跳转链接", blank=True)
    capture_username = models.BooleanField(default=False)
    capture_password = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "钓鱼页面"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name