from django.contrib import admin
from users.models import *
from dish.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )
    inlines = (BasketAdmin, )
