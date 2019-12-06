from django.db import models

# Create your models here.


################################################################################################################
## 联系人
################################################################################################################
class Linkman(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=20)
    email = models.EmailField(verbose_name="邮箱地址")
    department = models.CharField(verbose_name="部门", max_length=20)

    class Meta:
        verbose_name = "联系人"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


################################################################################################################
## 部门
#################################################################################################################
class Department(models.Model):
    name = models.CharField(verbose_name="部门名称")

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

##############################################################################################################
## 分组
##############################################################################################################
class Group(models.Model):
    name = models.CharField(verbose_name="分组名称")

    class Meta:
        verbose_name = "小组"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name