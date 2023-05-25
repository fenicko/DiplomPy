from django.shortcuts import render, HttpResponseRedirect

from dish.models import *

# Create your views here.


def index(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'dish/html/index.html', context=context)


def dishes(request):
    context = {
        'title': 'Dishes',
        'dish': Dish.objects.all(),
        'type': TypeDish.objects.all(),
        'struct': Structure.objects.all(),
    }
    return render(request, 'dish/html/dishs.html', context=context)


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

def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
