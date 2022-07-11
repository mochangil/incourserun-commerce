from django.contrib import admin
from . import models
from django.utils.html import mark_safe
from django.db.models import OuterRef, Exists
from .models import Photo


class PhotoInline(admin.TabularInline):
    model = models.Photo

class ReplyInline(admin.TabularInline):
    model = models.Reply

class HasPhotoFilter(admin.SimpleListFilter):
    title = '포토리뷰'
    parameter_name = 'has_photo'

    def lookups(self, request, model_admin):
        return(
            ("True", "True"),
            ("False", "False")
        )

    def queryset(self, request, queryset):
        photo_subquery = Photo.objects.filter(review=OuterRef('id')).values('review')
        if self.value() == "True":
            return queryset.annotate(has_photo = Exists(photo_subquery)).filter(has_photo = True)
        if self.value() == "False":
            return queryset.annotate(has_photo = Exists(photo_subquery)).filter(has_photo = False)


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
    list_filter = ('product', 'rating', HasPhotoFilter)
    search_fields = ("=user__name", "^user__email", "product__name", "content")

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = "사진 개수"

    def has_reply(self, obj):
        return hasattr(obj, 'reply')
    has_reply.short_description = "답글 등록 여부"
    has_reply.boolean = True

    def has_photo(self, obj):
        return obj.photos.exists()
    has_photo.short_description = "포토리뷰"
    has_photo.boolean = True


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

