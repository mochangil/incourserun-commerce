# Generated by Django 3.2.7 on 2022-07-01 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20220627_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_others', models.TextField(max_length=1000, null=True, verbose_name='기타사유')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='탈퇴일시')),
            ],
            options={
                'verbose_name': '회원탈퇴',
                'verbose_name_plural': '회원탈퇴',
            },
        ),
        migrations.CreateModel(
            name='WithdrawalReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.reason')),
                ('reasons', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.withdrawal')),
            ],
        ),
        migrations.AddField(
            model_name='withdrawal',
            name='reasons',
            field=models.ManyToManyField(through='user.WithdrawalReason', to='user.Reason', verbose_name='탈퇴사유'),
        ),
        migrations.AddField(
            model_name='withdrawal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal', to=settings.AUTH_USER_MODEL),
        ),
    ]
