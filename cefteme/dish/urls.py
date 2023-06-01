from django.urls import path

from dish.views import *

app_name = 'dish'

urlpatterns = [
    path('', dishes, name='index'),
    path('dish/<slug:dish_slug>', dish, name='dish'),
    path('type/<slug:type_slug>/', dishes, name='type'),
    path('page/<int:page_number>/', dishes, name='paginator'),
    path('baskets/add/<int:dish_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
