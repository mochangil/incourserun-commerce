from django.contrib import admin
from . import models
from django.utils.html import mark_safe


class PhotoInline(admin.TabularInline):
    model = models.Photo

class ReplyInline(admin.TabularInline):
    model = models.Reply


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = (PhotoInline, ReplyInline)
    list_display =  (
        'id',
        'user',
        'product',
        'order_product',
        'rating',
        'content',
        'count_photos',
        'has_photo',
        'has_reply',
        'created_at',
    )
    list_filter = ('product', 'rating')

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = "사진 개수"

    def has_photo(self, obj):
        return obj.photos.count() > 0
    has_photo.short_description = "포토리뷰"
    has_photo.boolean = True

    def has_reply(self, obj):
        return hasattr(obj, 'reply')
    has_reply.short_description = "답글 등록 여부"
    has_reply.boolean = True


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'get_img',
    )
    def get_img(self, obj):
        url = obj.img.url if obj.img else ""
        return mark_safe(f'<div> <div><a href="{url}">{obj.img}</a></div> <img width="100px" src="{url}" /> </div>')
    get_img.short_description = "이미지"


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'content',
        'created_at',
    )

