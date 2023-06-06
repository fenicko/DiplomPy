# Generated by Django 4.2.1 on 2023-06-06 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dish', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dish.menu'),
        ),
        migrations.AddField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(through='dish.MenuItem', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='menu',
            name='weekday',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dish.weekday'),
        ),
        migrations.AddField(
            model_name='dishcomplexdish',
            name='complex_dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dish.complexdish'),
        ),
        migrations.AddField(
            model_name='dishcomplexdish',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dish.dish'),
        ),
        migrations.AddField(
            model_name='dish',
            name='id_type_dish',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dish.typedish'),
        ),
        migrations.AddField(
            model_name='basket',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='basket',
            name='users',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
