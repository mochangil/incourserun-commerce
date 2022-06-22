# Generated by Django 3.2.7 on 2022-06-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address_detail',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='상세주소'),
        ),
        migrations.AddField(
            model_name='user',
            name='zipcode',
            field=models.CharField(blank=True, max_length=7, null=True, verbose_name='우편번호'),
        ),
    ]
