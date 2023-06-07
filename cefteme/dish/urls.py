from django.urls import path

from dish.views import *

app_name = 'dish'

urlpatterns = [
    path('', dishes, name='index'),
    path('type/<slug:type_slug>/', dishes, name='type'),
    path('weekday/<slug:weekday_slug>/', dishes, name='weekday'),
    path('type/<slug:type_slug>/weekday/<slug:weekday_slug>/', dishes, name='type_and_weekday'),
    path('dish/<slug:dish_slug>/', dish, name='dish'),
    path('dish/<slug:dish_slug>/action_ingredient/<int:ingredient_id>/', action_ingredient, name='action_ingredient'),
    path('dish/<slug:dish_slug>/dish_add/<int:dish_id>/', action_dish, name='action_dish'),
    path('baskets/add/<slug:dish_slug>/', basket_add, name='basket_add'),
    path('baskets/update/', basket_update, name='basket_update'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('order/', order, name='order'),
]
