from django.db import models
from django.core import serializers
from django.urls import reverse
from django.db.models import Count, Sum, Avg, Func

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from decimal import Decimal

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
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    quantity = models.PositiveIntegerField(default=0)
    baskets = GenericRelation('Basket')

    def get_ingredients(self):
        # Получаем все связанные ингредиенты для данного блюда
        structure_items = Structure.objects.filter(id_dish=self)
        ingredients = [item.id_ingredient for item in structure_items]
        return ingredients

    def __str__(self):
        return f'Блюдо: {self.name} | Категория: {self.id_type_dish.name}'

    def get_absolute_url(self):
        return reverse('dishes:dish', kwargs={'dish_slug': self.slug})

    def filter_ingredients(self):
        ingredients = Structure.objects.filter(id_dish=self.pk).values('id_ingredient')
        not_match_ingredients = Ingredients.objects.exclude(structure__id_dish=self.pk, structure__id_ingredient__in=ingredients)
        return not_match_ingredients


class ComplexDish(models.Model):
    name = models.CharField(max_length=182, null=True)
    image = models.ImageField(upload_to='dishes_images')
    quantity = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    baskets = GenericRelation('Basket')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dishes:dish', kwargs={'dish_slug': self.slug})

    def get_dishes(self):
        dish_ids = DishComplexDish.objects.filter(complex_dish=self).values_list('dish', flat=True)
        return Dish.objects.filter(id__in=dish_ids)

    def get_unrelated_dishes(self):
        return Dish.objects.exclude(dishcomplexdish__complex_dish=self)

    def calculate_complex_dish_price(self):
        dish_complexes = DishComplexDish.objects.filter(complex_dish=self)
        total_price = dish_complexes.aggregate(Sum('dish__price'))['dish__price__sum']
        return total_price


class DishComplexDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)
    complex_dish = models.ForeignKey(ComplexDish, on_delete=models.PROTECT)

    def __str__(self):
        return f'Блюдо: {self.dish.name} | {self.complex_dish.name}'

    class Meta:
        db_table = 'dish_complex_dish'


class TypeDish(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dish:type', kwargs={'type_slug': self.slug})


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum_dish() + basket.sum_complex_dish() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    users = models.ForeignKey(User, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        dish = self.content_object
        return f'Блюдо: {dish.name} | Меню: {self.users.username}'

    def sum_dish(self):
        return self.content_object.price * Decimal(self.quantity)

    def sum_complex_dish(self):
        price = self.content_object.calculate_complex_dish_price()
        return price * Decimal(self.quantity)

    def get_sum(self):
        return self.sum_dish() + self.sum_complex_dish()

    def get_total_sum(self):
        return self.sum_dish() + self.sum_complex_dish()

    def get_content_object_model_name(self):
        return self.content_type.model_class()._meta.model_name


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


class Reviews(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.PROTECT)
    id_dish = models.ForeignKey(Dish, on_delete=models.PROTECT, null=True)
    id_comp_dish = models.ForeignKey(ComplexDish, on_delete=models.PROTECT, null=True)
    estimation = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Пользователь: {self.id_user.username} | Оценка: {self.estimation}'

    @classmethod
    def get_estimation_sum_per_dish(cls):
        return cls.objects.values('id_dish').annotate(total_estimation=Sum('estimation'), count_estimation=Count('estimation')).annotate(average_estimation=Round(Avg('estimation')))

    @classmethod
    def get_estimation_sum_per_comp_dish(cls):
        return cls.objects.values('id_comp_dish').annotate(total_estimation=Sum('estimation'), count_estimation=Count('estimation')).annotate(average_estimation=Round(Avg('estimation')))


class Weekday(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=182, null=True)
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    items = models.ManyToManyField(ContentType, through='MenuItem')

    def __str__(self):
        return self.name

    def get_dishes_for_weekday(self, weekday_name):
        weekday = Weekday.objects.get(name=weekday_name)
        menu_items = MenuItem.objects.filter(menu=self, menu__weekday=weekday)
        dishes = [menu_item.content_object for menu_item in menu_items.filter()]
        return dishes


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    dish_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'dish_id')

    def __str__(self):
        dish = self.content_object
        return f'Блюдо: {dish.name} | Меню: {self.menu.name}'


