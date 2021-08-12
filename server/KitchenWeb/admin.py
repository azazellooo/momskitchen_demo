from django.contrib import admin
from .models import Category, Supplement, Dish, Garnish, Additional, Offering


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


class GarnishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order', 'base_price', 'extra_price']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['id', 'name', 'order', 'base_price', 'extra_price']
    readonly_fields = ['id', ]

class AdditionalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sampling_order', 'base_price', 'extra_price']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['id', 'name', 'sampling_order', 'base_price', 'extra_price']
    readonly_fields = ['id', ]


class OfferingAdmin(admin.ModelAdmin):
    list_display = ['id', 'position', 'qty_portion', 'date', 'special_offering', 'discount']
    list_filter = ['date']
    search_fields = ['position']
    fields = ['id', 'position', 'garnish', 'supplement', 'additional', 'qty_portion', 'date', 'special_offering', 'discount']
    readonly_fields = ['id', ]



admin.site.register(Dish, DishAdmin)
admin.site.register(Supplement, SupplementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Garnish, GarnishAdmin)
admin.site.register(Additional, AdditionalAdmin)
admin.site.register(Offering, OfferingAdmin)

