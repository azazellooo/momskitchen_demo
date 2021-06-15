from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'order']
    list_filter = ['category_name']
    search_fields = ['category_name']
    fields = ['id', 'category_name', 'order']
    readonly_fields = ['id']

admin.site.register(Category, CategoryAdmin)
