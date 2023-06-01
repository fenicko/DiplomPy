from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, F

from dish.forms import *
from dish.models import *

# Create your views here.


def index(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'dish/html/index.html', context=context)


def dishes(request, type_slug=None, page_number=1):
    dishes = Dish.objects.filter(id_type_dish__slug=type_slug) if type_slug else Dish.objects.all()
    estimation_sum_per_dish = Reviews.get_estimation_sum_per_dish()


    per_page = 3
    paginator = Paginator(dishes, per_page)
    dishes_paginator = paginator.page(page_number)

    context = {'title': 'Dishes',
               'type': TypeDish.objects.all(),
               'struct': Structure.objects.all(),
               'dish': dishes_paginator,
               'review': Reviews.objects.all(),
               'review_counts': estimation_sum_per_dish,
               }
    return render(request, 'dish/html/dishs.html', context=context)


def dish(request, dish_slug):
    post = get_object_or_404(Dish, slug=dish_slug)

    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            try:
                Reviews.objects.create(id_user=request.user, id_dish=post, **form.cleaned_data)
                return redirect('dishes:dish', dish_slug)
            except:
                form.add_error(None, 'Ошибка добавления коментария')
    else:
        form = AddReviewForm()

    context = {
        'title': 'Dish',
        'dish': post,
        'review': Reviews.objects.all(),
        'form': form
    }

    return render(request, 'dish/html/dish.html', context=context)


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


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')