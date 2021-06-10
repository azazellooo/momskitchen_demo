from django.contrib import admin
from accounts.models import Organization, Users, UserToken
from kitchen5bot.models import TelegramUser
# Register your models here.

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'secondary_key', 'generate_link']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['id', 'name', 'secondary_key']
    readonly_fields = ['id', 'secondary_key']


class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'organization_id', 'username']
    list_filter = ['organization_id']
    search_fields = ['organization_id', 'username']
    fields = ['id', 'tg_user', 'organization_id', 'username']
    readonly_fields = ['id']


class UserTgAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'is_bot', 'username']
    list_filter = ['telegram_id', 'is_bot', 'username']
    search_fields = ['telegram_id', 'first_name', 'last_name', 'username']
    fields = ['id', 'telegram_id', 'is_bot', 'first_name', 'last_name', 'username']
    readonly_fields = ['id']


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'user']
    readonly_fields = ['id', 'key']

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(TelegramUser, UserTgAdmin)
admin.site.register(UserToken, UserTokenAdmin)