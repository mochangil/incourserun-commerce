# Generated by Django 3.2.7 on 2022-06-20 12:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20220620_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='capacity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='용량'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='가격'),
        ),
    ]
