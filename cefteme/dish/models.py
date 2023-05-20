from django.db import models

# Create your models here.


class Ingredients(models.Model):
    name = models.CharField(max_length=128)


class Structure(models.Model):
    id_dish = models.ForeignKey('Dish', on_delete=models.PROTECT, unique=True, null=True)
    id_ingredient = models.ForeignKey(Ingredients, on_delete=models.PROTECT, unique=True, null=True)


class Dish(models.Model):
    id_type_dish = models.ForeignKey('TypeDish', on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to='dishes_images')
    price = models.DecimalField(max_digits=6, decimal_places=2)


class TypeDish(models.Model):
    name = models.CharField(max_length=128)


class Сheque(models.Model):
    price_cheque = models.DecimalField(max_digits=6, decimal_places=2)
    set_menu = models.BooleanField()


class SetMenu(models.Model):
    id_menu = models.ForeignKey(Сheque, on_delete=models.PROTECT, null=True)
    id_dish = models.ForeignKey(Dish, on_delete=models.PROTECT, null=True)


class Order(models.Model):
    id_cheque = models.ForeignKey('Сheque', on_delete=models.PROTECT, null=True)
    id_user_cheque = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
    date_order = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    lastname = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    login = models.CharField(max_length=128)


class RoleUser(models.Model):
    id_role = models.ForeignKey('Role', on_delete=models.PROTECT, unique=True, null=True)
    id_user = models.ForeignKey(User, on_delete=models.PROTECT, unique=True, null=True)


class Role(models.Model):
    name = models.CharField(max_length=128)


class Classes(models.Model):
    name = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField(default=0)
    id_responsible = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
