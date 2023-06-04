from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, F

from django.http import JsonResponse
import json

from dish.forms import *
from dish.models import *

# Create your views here.


def index(request):
    return render(request, 'dish/html/index2.html')


def dishes(request, type_slug=None):
    dishes = Dish.objects.filter(id_type_dish__slug=type_slug) if type_slug else Dish.objects.all()
    estimation_sum_per_dish = Reviews.get_estimation_sum_per_dish()

    per_page = 6
    paginator = Paginator(dishes, per_page)

    page_number = request.GET.get('page')
    page_dish = paginator.get_page(page_number)

    context = {
               'type': TypeDish.objects.all(),
               'dish': page_dish,
               'review': Reviews.objects.all(),
               'review_counts': estimation_sum_per_dish,
               }
    return render(request, 'dish/html/dishes2.html', context=context)


def action_ingredient(request, dish_slug, ingredient_id):
    ingredient = Ingredients.objects.get(pk=ingredient_id)
    dish = Dish.objects.get(slug=dish_slug)

    struct = Structure.objects.filter(id_dish_id=dish.pk, id_ingredient_id=ingredient.pk)
    if not struct:
        Structure.objects.create(id_dish_id=dish.pk, id_ingredient_id=ingredient.pk)
    else:
        struct = struct.first()
        struct.delete()

    return HttpResponseRedirect(reverse('dish:dish', args=[dish_slug]))


def dish(request, dish_slug):
    post = get_object_or_404(Dish, slug=dish_slug)
    estimation_sum_per_dish = Reviews.get_estimation_sum_per_dish()

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
        'dish': post,
        'review': Reviews.objects.all(),
        'review_counts': estimation_sum_per_dish,
        'form': form,
    }

    return render(request, 'dish/html/dish2.html', context=context)


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


def basket_update(request):
    if request.method == 'POST':
        basket_id = request.POST.get('basketId')
        quantity = request.POST.get('quantity')

        # Обновите запись в БД с использованием полученных данных
        basket = get_object_or_404(Basket, pk=basket_id)
        basket.quantity = quantity
        basket.save()

        updated_sum = basket.sum()

        response_data = {'success': True, 'updated_sum': updated_sum}
        return JsonResponse(response_data)
    else:
        response_data = {'success': False}
        return JsonResponse(response_data)


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(reverse('users:profile'))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
