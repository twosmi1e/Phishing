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

    def get_email_list(self):
        email_list = []
        for m in self.group_members.all():
            email_list.append(m.email)
        return email_list

    def get_name_list(self):
        name_list = []
        for m in self.group_members.all():
            name_list.append(m.name)
        return name_list

    def get_id_email_dict(self):
        id_email_dict = []
        for m in self.group_members.all():
            id_email_dict.append((m.id, m.email))
        return id_email_dict

    def __str__(self):
        return self.name
