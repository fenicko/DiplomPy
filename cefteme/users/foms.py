from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import *
from dish.models import *


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        filter = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'u-grey-5 u-input u-input-rectangle u-radius-50'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'u-grey-5 u-input u-input-rectangle u-radius-50'}))
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'u-grey-5 u-input u-input-rectangle u-radius-50', 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'u-grey-5 u-input u-input-rectangle u-radius-50'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')

