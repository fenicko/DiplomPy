from django.urls import path

from dish.views import *

app_name = 'dish'

urlpatterns = [
    path('', dishes, name='index')
]
