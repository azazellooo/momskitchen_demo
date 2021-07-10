from django.contrib import admin
from accounts.models import Organization, UserToken, BalanceChange, Employe
from kitchen5bot.models import TelegramUser

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'secondary_key', 'generate_link']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['id', 'name', 'secondary_key']
    readonly_fields = ['id', 'secondary_key']


class EmployeAdmin(admin.ModelAdmin):
    list_display = ['id', 'tg_user', 'organization_id', 'username', 'is_active', 'total_balance', 'is_admin']
    list_filter = ['organization_id']
    search_fields = ['organization_id', 'username']
    fields = ['id', 'tg_user', 'organization_id', 'username', 'is_active', 'total_balance', 'is_admin']
    readonly_fields = ['id']


class UserTgAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'is_bot', 'username']
    list_filter = ['telegram_id', 'is_bot', 'username']
    search_fields = ['telegram_id', 'first_name', 'last_name', 'username']
    fields = ['id', 'telegram_id', 'is_bot', 'first_name', 'last_name', 'username']
    readonly_fields = ['id']


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'user', 'created_at']
    readonly_fields = ['id', 'key', 'created_at']


class BalanceChangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'employe', 'sum_balance', 'created_at', 'balance_after_transaction']
    list_filter = ['type', 'employe']
    search_fields = ['type', 'employe']
    fields = ['id', 'type', 'employe', 'sum_balance', 'comment', 'created_at']
    readonly_fields = ['id', 'created_at']



admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Employe, EmployeAdmin)
admin.site.register(TelegramUser, UserTgAdmin)
admin.site.register(UserToken, UserTokenAdmin)
admin.site.register(BalanceChange, BalanceChangeAdmin)