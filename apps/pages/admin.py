from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'redirect_url', 'add_time')