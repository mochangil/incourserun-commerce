# Generated by Django 3.2.7 on 2022-06-20 11:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='deleted',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=1000, verbose_name='주소'),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.CharField(blank=True, choices=[('teen', '10대'), ('twenty', '20대'), ('thirty', '30대'), ('forty', '40대'), ('fifty', '50대 이상')], max_length=6, verbose_name='연령대'),
        ),
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='가입일시'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', '남성'), ('female', '여성')], max_length=6, verbose_name='성별'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_register',
            field=models.BooleanField(default=False, verbose_name='등록여부'),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='닉네임'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to=None, verbose_name='프로필사진'),
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('kakao', '카카오'), ('naver', '네이버'), ('facebook', '페이스북'), ('google', '구글'), ('apple', '애플')], max_length=16, verbose_name='타입')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '소셜',
                'verbose_name_plural': '소셜',
            },
        ),
    ]