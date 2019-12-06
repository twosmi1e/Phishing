from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Linkman)
class LinkmanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'department')

