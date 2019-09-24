# Generated by Django 2.2.5 on 2019-09-24 03:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_remove_recipe_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
