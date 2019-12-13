from django.db import models


# Create your models here.

################################################################################################################
## 部门
#################################################################################################################
class Department(models.Model):
    name = models.CharField(verbose_name="部门名称", max_length=40)

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


################################################################################################################
## 联系人
################################################################################################################


class Linkman(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=20)
    email = models.EmailField(verbose_name="邮箱地址")
    depart = models.ForeignKey(Department, verbose_name="部门", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "联系人"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


##############################################################################################################
## 分组
##############################################################################################################
class Group(models.Model):
    name = models.CharField(verbose_name="分组名称", max_length=20)
    group_members = models.ManyToManyField(Linkman)

    class Meta:
        verbose_name = "分组"
        verbose_name_plural = verbose_name

    def get_members(self):
        return "\n".join([m.name for m in self.group_members.all()])

    def __str__(self):
        return self.name
