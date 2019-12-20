########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.urls import path


########################################################################################################################
## 系统自带模块导入
########################################################################################################################
from .views import *
########################################################################################################################
## 自建模块导入
########################################################################################################################


########################################################################################################################
## url
########################################################################################################################
app_name = 'contacts'

urlpatterns = [
    # 联系人
    path('linkman/list', LinkmanListView.as_view(), name='linkman_list'),
    # 添加联系人
    path('linkman/add', AddLinkman.as_view(), name='add_linkman'),
    # 编辑联系人
    path('linkman/edit/<int:l_id>', EditLinkman.as_view(), name='edit_linkman'),
    # 删除联系人
    path('linkman/del/<int:l_id>', DeleteLinkman.as_view(), name='del_linkman'),
    # 部门
    path('depart/list', DepartListView.as_view(), name='depart_list'),
    # 添加部门
    path('depart/add', AddDepart.as_view(), name='add_depart'),
    # 编辑部门
    path('depart/edit/<int:d_id>', EditDepart.as_view(), name='edit_depart'),
    # 删除部门
    path('depart/del/<int:d_id>', DeleteDepart.as_view(), name='del_depart'),
    # 分组
    path('group/list', GroupListView.as_view(), name='group_list'),
    # 添加分组
    path('group/add', AddGroup.as_view(), name='add_group'),
    # 删除分组
    path('group/del/<int:g_id>', DeleteGroup.as_view(), name='del_group'),
]


