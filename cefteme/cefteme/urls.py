from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from dish.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('dishes/', include('dish.urls', namespace='dishes')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/dish/dish/<int:record_id>/change/', edit_record, name='edit_record'),
    path('admin/dish/dish/add/', add_dish, name='add_dish'),
    path('admin/dish/complexdish/add/', add_dish, name='add_comp_dish'),
    path('admin/dish/dish/', del_dish, name='del_dish'),
]

handler404 = pageNotFound

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
