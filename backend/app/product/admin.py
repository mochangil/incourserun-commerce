from django.contrib import admin
from django.utils.html import mark_safe

from . import models


# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'capacity',
        'price',
        'description',
        'get_thumbnail_img',
        'get_product_img',
        'get_detail_img',
        'created_at',
    )

    def get_thumbnail_img(self, obj):
        url = obj.thumbnail_img.url if obj.thumbnail_img else ""
        return mark_safe(
            f'<div> <div><a href="{url}">{obj.thumbnail_img}</a></div> <img width="100px" src="{url}" /> </div>')

    get_thumbnail_img.short_description = "썸네일이미지"

    def get_product_img(self, obj):
        url = obj.product_img.url if obj.product_img else ""
        return mark_safe(
            f'<div> <div><a href="{url}">{obj.product_img}</a></div> <img width="100px" src="{url}" /> </div>')

    get_product_img.short_description = "상품이미지"

    def get_detail_img(self, obj):
        url = obj.detail_img.url if obj.detail_img else ""
        return mark_safe(
            f'<div> <div><a href="{url}">{obj.detail_img}</a></div> <img width="100px" height="200px" src="{url}" /> </div>')

    get_detail_img.short_description = "상세이미지"


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
