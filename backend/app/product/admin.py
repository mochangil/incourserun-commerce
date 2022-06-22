from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'capacity',
        'description',
        'product_img',
        'detail_img',
        'created',
    )


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)