from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Linkman)
class LinkmanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'depart')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ['name', 'group_members']
    list_display = ('id', 'name', 'get_members')

