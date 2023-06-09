from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from dish.models import Basket
from users.foms import *


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/registration.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserProfileForm(instance=request.user)

    basket = BasketItem.objects.first()  # Получаем объект корзины
    if basket:
        model_name = basket.content_type.model_class()._meta.model_name
    else:
        model_name = None

    context = {'title': 'Профиль',
               'form': form,
               'model_name': model_name,
               'baskets': BasketItem.objects.filter(basket__users=request.user, basket__its_bay=False),
               'its_bay': Basket.objects.filter(users=request.user),
               }
    return render(request, 'users/profile2.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
