# Generated by Django 3.2.7 on 2022-06-20 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_request',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='배송요청사항'),
        ),
    ]
