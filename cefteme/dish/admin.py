from django.contrib import admin

from dish.models import *

admin.site.register(Ingredients)
admin.site.register(Dish)
admin.site.register(Structure)
admin.site.register(TypeDish)
