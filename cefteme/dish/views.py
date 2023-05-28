from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from dish.models import *

# Create your views here.


def index(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'dish/html/index.html', context=context)


def dishes(request, type_id=None, page_number=1):
    dishes = Dish.objects.filter(id_type_dish=type_id) if type_id else Dish.objects.all()

    per_page = 3
    paginator = Paginator(dishes, per_page)
    dishes_paginator = paginator.page(page_number)

    context = {'title': 'Dishes',
               'type': TypeDish.objects.all(),
               'struct': Structure.objects.all(),
               'dish': dishes_paginator,
               }
    return render(request, 'dish/html/dishs.html', context=context)


@login_required
def basket_add(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    baskets = Basket.objects.filter(users=request.user, dish=dish)

    if not baskets.exists():
        Basket.objects.create(users=request.user, dish=dish, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
