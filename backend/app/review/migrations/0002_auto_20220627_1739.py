# Generated by Django 3.2.7 on 2022-06-27 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='created',
            new_name='created_at',
        ),
    ]
