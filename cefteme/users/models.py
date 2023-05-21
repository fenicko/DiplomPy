from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='user_image', null=True, blank=True)


# class RoleUser(models.Model):
#     id_role = models.ForeignKey('Role', on_delete=models.PROTECT, unique=True, null=True)
#     id_user = models.ForeignKey(User, on_delete=models.PROTECT, unique=True, null=True)
#
#
# class Role(models.Model):
#     name = models.CharField(max_length=128)
#
#     def __str__(self):
#         return self.name
#
#
# class Classes(models.Model):
#     name = models.CharField(max_length=128)
#     quantity = models.PositiveIntegerField(default=0)
#     id_responsible = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
#
#     def __str__(self):
#         return self.name
