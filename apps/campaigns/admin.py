from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_date', 'group', 'page', 'server', 'header')


