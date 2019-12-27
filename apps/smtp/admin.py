from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(EmailServer)
class EmailServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'interface', 'host', 'port', 'mail_user', 'mail_pass')