from django.contrib import admin

from dish.models import *

admin.site.register(Ingredients)
admin.site.register(Structure)
admin.site.register(Reviews)


@admin.register(TypeDish)
class TypeDishAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'id_type_dish')
    fields = ('name', 'slug', 'id_type_dish', 'image', 'price')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ('name',)}


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('dish', 'quantity', 'create_timestamp')
    readonly_fields = ('create_timestamp',)
    extra = 0
