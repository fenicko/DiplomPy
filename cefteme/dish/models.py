from django.db import models
from django.core import serializers

import users.models
from users.models import *
# Create your models here.


class Ingredients(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Structure(models.Model):
    id_dish = models.ForeignKey('Dish', on_delete=models.PROTECT, null=True)
    id_ingredient = models.ForeignKey(Ingredients, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'Блюдо: {self.id_dish.name} | Ингридиент: {self.id_ingredient.name}'


class Dish(models.Model):
    name = models.CharField(max_length=182, null=True)
    id_type_dish = models.ForeignKey('TypeDish', on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to='dishes_images')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def get_ingredients(self):
        # Получаем все связанные ингредиенты для данного блюда
        structure_items = Structure.objects.filter(id_dish=self)
        ingredients = [item.id_ingredient for item in structure_items]
        return ingredients

    def __str__(self):
        return f'Блюдо: {self.name} | Категория: {self.id_type_dish.name}'


class TypeDish(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.users.username} | Блюдо: {self.dish.name}'

    def sum(self):
        return self.dish.price * self.quantity
