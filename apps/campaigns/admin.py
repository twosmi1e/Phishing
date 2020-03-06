from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    fields = ['name', 'group', 'templet', 'page', 'servers', 'header']
    list_display = ('id', 'name', 'group', 'templet', 'page', 'get_servers', 'header')


