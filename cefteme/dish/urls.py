from django.urls import path

from dish.views import *

app_name = 'dish'

urlpatterns = [
    path('', dishes, name='index'),
    path('baskets/add/<int:dish_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
