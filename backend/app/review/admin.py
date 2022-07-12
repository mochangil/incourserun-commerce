from django.contrib import admin
from django.utils.html import mark_safe
from django.db.models import OuterRef, Exists, Q
from .models import Review, Photo, Reply


class PhotoInline(admin.TabularInline):
    model = Photo

class ReplyInline(admin.TabularInline):
    model = Reply

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


class HasReplyFilter(admin.SimpleListFilter):
    title = '답글 유무'
    parameter_name = 'has_reply'

    def lookups(self, request, model_admin):
        return(
            ("True", "True"),
            ("False", "False")
        )

    def queryset(self, request, queryset):
        reply_subquery = Reply.objects.filter(review=OuterRef('id')).values('review')
        if self.value() == 'True':
            return queryset.annotate(has_reply = Exists(reply_subquery)).filter(has_reply = True)
        if self.value() == 'False':
            return queryset.annotate(has_reply = Exists(reply_subquery)).filter(has_reply = False)


class HasContentFilter(admin.SimpleListFilter):
    title = '내용 유무'
    parameter_name = 'content'

    def lookups(self, request, model_admin):
        return(
            ("True", "True"),
            ("False", "False")
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.exclude(content__isnull=True).exclude(content__exact='')
        if self.value() == 'False':
            return queryset.filter(Q(content__isnull=True) | Q(content__exact=''))


@admin.register(Review)
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
    list_filter = ('product', 'rating', HasPhotoFilter, HasReplyFilter, HasContentFilter)
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


@admin.register(Photo)
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


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'content',
        'created_at',
    )

