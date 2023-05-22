from django.shortcuts import render

from dish.models import *

# Create your views here.


def index(request):
    context = {
        'title': 'Home dish',
    }
    return render(request, 'dish/html/index.html', context=context)


def dishes(request):
    context = {
        'title': 'Dishes',
        'dish': Dish.objects.all(),
        'struct': Structure.objects.all(),
        'category': TypeDish.objects.all(),
    }
    return render(request, 'dish/html/dishs.html', context=context)
