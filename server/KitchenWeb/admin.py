from django.contrib import admin
from .models import Category, Supplement, Dish


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'order']
    list_filter = ['category_name']
    search_fields = ['category_name']
    fields = ['id', 'category_name', 'order']
    readonly_fields = ['id']


class SupplementAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['id', 'name', 'price']
    readonly_fields = ['id', ]

class DishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'image', 'base_price', 'extra_price']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['id', 'name', 'description', 'category', 'image', 'base_price', 'extra_price']
    readonly_fields = ['id', ]


admin.site.register(Dish, DishAdmin)
admin.site.register(Supplement, SupplementAdmin)
admin.site.register(Category, CategoryAdmin)
