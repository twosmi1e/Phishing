from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Templet)
class TempletAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'attachments', 'add_time')