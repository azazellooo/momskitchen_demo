from django.contrib import admin
from accounts.models import Organization, Users
from kitchen5bot.models import TelegramUser
# Register your models here.

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'secondary_key']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['id', 'name', 'secondary_key']
    readonly_fields = ['id', 'secondary_key']


class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'organization_id']
    list_filter = ['organization_id']
    search_fields = ['organization_id']
    fields = ['id', 'tg_user', 'organization_id']
    readonly_fields = ['id']


class UserTgAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'is_bot', 'username']
    list_filter = ['telegram_id', 'is_bot', 'username']
    search_fields = ['telegram_id', 'first_name', 'last_name', 'username']
    fields = ['id', 'telegram_id', 'is_bot', 'first_name', 'last_name', 'username']
    readonly_fields = ['id']

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(TelegramUser, UserTgAdmin)