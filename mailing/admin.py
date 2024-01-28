from django.contrib import admin
from mailing.models import Client, Message, Mailing, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Mailing)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'interval', 'status',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'last_mailing_time', 'status',)
