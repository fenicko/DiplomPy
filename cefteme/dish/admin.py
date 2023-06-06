from django.contrib import admin

from dish.models import *

admin.site.register(Ingredients)
admin.site.register(Structure)
admin.site.register(Reviews)
admin.site.register(DishComplexDish)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('menu', 'content_object')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'weekday')


@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ('name',)}


@admin.register(ComplexDish)
class ComplexDishAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ('name',)}


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
    fields = ('dish_object', 'quantity', 'create_timestamp')
    readonly_fields = ('create_timestamp',)
    extra = 0
