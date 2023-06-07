from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, F
from datetime import datetime

from django.http import JsonResponse
import json

from dish.forms import *
from dish.models import *
from django.db.models.signals import pre_delete

weekday_names = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
get_index_weekday = 1


def index(request):
    return render(request, 'dish/html/index2.html')


def dishes(request, type_slug=None, weekday_slug=None):
    today = datetime.now().weekday()

    if weekday_slug:
        day = Weekday.objects.get(slug=weekday_slug)
        today_name = weekday_names[day.pk - get_index_weekday]
    else:
        today_name = weekday_names[today]

    menu = Menu.objects.get(weekday__name=today_name)
    dishes_for_today = menu.get_dishes_for_weekday(today_name)

    per_page = 6
    if type_slug == 'complex':
        comp_dish_slugs = [comp_dish.slug for comp_dish in dishes_for_today]
        comp_dishes = ComplexDish.objects.filter(slug__in=comp_dish_slugs)
        paginator = Paginator(comp_dishes, per_page)
        estimation_sum_per_dish = Reviews.get_estimation_sum_per_comp_dish()
        select_model = 'complex'
    else:
        dish_ids = [dish.slug for dish in dishes_for_today]
        dishes = Dish.objects.filter(slug__in=dish_ids, id_type_dish__slug=type_slug) if type_slug else Dish.objects.filter(slug__in=dish_ids)
        paginator = Paginator(dishes, per_page)
        estimation_sum_per_dish = Reviews.get_estimation_sum_per_dish()
        select_model = 'dish'

    page_number = request.GET.get('page')
    page_dish = paginator.get_page(page_number)

    context = {
               'type': TypeDish.objects.all(),
               'weekday': today_name,
               'weekdays': Weekday.objects.all(),
               'model': page_dish,
               'review': Reviews.objects.all(),
               'select_model': select_model,
               'review_counts': estimation_sum_per_dish,
               'get_type_slug': type_slug,
               'get_weekday_slug': weekday_slug,
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


def action_dish(request, dish_slug, dish_id):
    dish = Dish.objects.get(pk=dish_id)
    comp_dish = ComplexDish.objects.get(slug=dish_slug)

    struct = DishComplexDish.objects.filter(dish_id=dish.pk, complex_dish_id=comp_dish.pk)
    if not struct:
        DishComplexDish.objects.create(dish_id=dish.pk, complex_dish_id=comp_dish.pk)
    else:
        struct = struct.first()
        struct.delete()

    return HttpResponseRedirect(reverse('dish:dish', args=[dish_slug]))


def dish(request, dish_slug):
    try:
        post = Dish.objects.get(slug=dish_slug)
        select_model = 'dish'
        review_sum = Reviews.get_estimation_sum_per_dish()
    except Dish.DoesNotExist:
        try:
            post = ComplexDish.objects.get(slug=dish_slug)
            select_model = 'complex'
            review_sum = Reviews.get_estimation_sum_per_comp_dish()
        except ComplexDish.DoesNotExist:
            return HttpResponseNotFound("Dish not found")

    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            try:
                if select_model == 'dish':
                    Reviews.objects.create(id_user=request.user, id_dish=post, **form.cleaned_data)
                elif select_model == 'complex':
                    Reviews.objects.create(id_user=request.user, id_comp_dish=post, **form.cleaned_data)
                return redirect('dishes:dish', dish_slug)
            except:
                form.add_error(None, 'Ошибка добавления комментария')
    else:
        form = AddReviewForm()

    context = {
        'dish': post,
        'review': Reviews.objects.all(),
        'review_counts': review_sum,
        'form': form,
        'select_model': select_model,
    }

    return render(request, 'dish/html/dish2.html', context=context)


@login_required
def basket_add(request, dish_slug):
    try:
        dish = Dish.objects.get(slug=dish_slug)
        content_type = ContentType.objects.get_for_model(Dish)
        content_object = dish
    except Dish.DoesNotExist:
        try:
            dish = ComplexDish.objects.get(slug=dish_slug)
            content_type = ContentType.objects.get_for_model(ComplexDish)
            content_object = dish
        except ComplexDish.DoesNotExist:
            return HttpResponseNotFound("Dish not found")

    basket, created = Basket.objects.get_or_create(
        users=request.user,
        its_bay=False,
    )

    basket_items = BasketItem.objects.filter(basket=basket, content_type=content_type, object_id=content_object.id)

    if not basket_items.exists():
        BasketItem.objects.create(basket=basket, content_type=content_type, object_id=content_object.id, quantity=1)
    else:
        basket_item = basket_items.first()
        basket_item.quantity += 1
        basket_item.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_update(request):
    if request.method == 'POST':
        basket_id = request.POST.get('basketId')
        quantity = request.POST.get('quantity')

        # Обновите запись в БД с использованием полученных данных
        basket = get_object_or_404(BasketItem, pk=basket_id)
        basket.quantity = quantity
        basket.save()

        updated_sum_dish = basket.get_dish_price()
        updated_sum_complex_dish = basket.get_complex_dish_price()
        total_sum = Decimal(updated_sum_dish + updated_sum_complex_dish).quantize(Decimal('0.00'))
        print(total_sum)

        response_data = {
            'sum_dish': updated_sum_dish,
            'sum_complex_dish': updated_sum_complex_dish,
            'total_sum': total_sum,
        }
        return JsonResponse(response_data)
    else:
        response_data = {'success': False}
        return JsonResponse(response_data)


@login_required
def basket_remove(request, basket_id):
    basket = BasketItem.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(reverse('users:profile'))


@login_required
def order(request):
    if request.method == 'POST':

        paragraph_content = request.POST.get('paragraph_content')
        clear_text = paragraph_content.replace(',', '.')
        total_price = Decimal(clear_text).quantize(Decimal('0.00'))

        user = request.user
        baskets = Basket.objects.get(users=user, its_bay=False)

        order = Order()
        order.user_id = user
        order.baskets = baskets
        order.code_order = Order.generate_code()
        order.price = total_price
        order.save()

        baskets.its_bay = True
        baskets.save()


    context = {
        'order': Order.objects.all(),
        'order_f': Order.objects.first(),
    }
    return render(request, 'dish/html/order.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
