from django.contrib import admin
from .models import Category, Supplement, Dish, Garnish, Additional, Offering, Cart, Order, OrderOffernig


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
    list_display = ['id', 'position', 'qty_portion', 'date']
    list_filter = ['date']
    search_fields = ['position']
    fields = ['id', 'position', 'qty_portion', 'date', 'supplement']
    readonly_fields = ['id', ]

# class OfferingGarnishAdmin(admin.ModelAdmin):
#     list_display = ['id', 'offering_id', 'garnish_id']
#     list_filter = ['offering_id']
#     search_fields = ['offering_id']
#     fields = ['id', 'offering_id', 'garnish_id']
#     readonly_fields = ['id']


class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'offering', 'user', 'is_confirmed', 'created_at']
    fields = ['id', 'offering', 'user', 'qty', 'price', 'portions', 'is_confirmed']
    search_fields = ['user']
    readonly_fields = ['id']


class OrderOffernigAdmin(admin.ModelAdmin):
    list_display = ['id', 'offering', 'order']
    fields = ['id', 'offering', 'order', 'qty', 'price', 'portions']
    search_fields = ['user']
    readonly_fields = ['id']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'is_delivered']
    fields = ['id', 'user', 'created_at', 'is_delivered']
    search_fields = ['user']
    readonly_fields = ['id', 'created_at']



admin.site.register(Dish, DishAdmin)
admin.site.register(Supplement, SupplementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Garnish, GarnishAdmin)
admin.site.register(Additional, AdditionalAdmin)
admin.site.register(Offering, OfferingAdmin)
admin.site.register(Cart, BasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderOffernig, OrderOffernigAdmin)
# admin.site.register(offerings_garnish)
