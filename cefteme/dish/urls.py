from django.urls import path

from dish.views import *

app_name = 'dish'

urlpatterns = [
    path('', dishes, name='index'),
    path('dish/<slug:dish_slug>/', dish, name='dish'),
    path('dish/<slug:dish_slug>/ingredient_add/<int:ingredient_id>/', action_ingredient, name='action_ingredient'),
    path('type/<slug:type_slug>/', dishes, name='type'),
    path('baskets/add/<int:dish_id>/', basket_add, name='basket_add'),
    path('baskets/update/', basket_update, name='basket_update'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
