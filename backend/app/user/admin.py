from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

from . import models
from ..cart.models import Cart
from ..order.models import Order
from ..review.models import Review


class CartInline(admin.TabularInline):
    model = Cart


class OrderInline(admin.TabularInline):
    model = Order


class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    inlines = (CartInline, OrderInline, ReviewInline)
    fieldsets = (
        ('Personal info',
         {'fields': (
             "username",
             "password",
             "name",
             "nickname",
             "email",
             "phone",
             "gender",
             "age_range",
             "zipcode",
             "address",
             "address_detail",
             "avatar",
             "is_active",
             "is_staff",
             "is_superuser",
             "is_register",
             "agree_all_terms",
             "required_terms",
             "private_info_terms",
             "marketing_terms",
         )}
         ),
    )
    list_filter = UserAdmin.list_filter + ('gender', 'age_range', 'is_register',)
    list_display = (
        "id",
        "username",
        "name",
        "nickname",
        "email",
        "phone",
        "get_avatar",
        "gender",
        "age_range",
        "zipcode",
        "address",
        "address_detail",
        "created_at",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_register",
        "agree_all_terms",
        "required_terms",
        "private_info_terms",
        "marketing_terms",
        "count_carts",
        "count_orders",
        "count_reviews",
    )
    search_fields = ("=name", "^email", "^phone", "=zipcode", "address", "address_detail",)

    def get_avatar(self, obj):
        url = obj.avatar.url if obj.avatar else ""
        return mark_safe(f'<div> <div><a href="{url}">{obj.avatar}</a></div> <img width="100px" src="{url}" /> </div>')

    get_avatar.short_description = "프로필사진"

    def count_carts(self, obj):
        return obj.carts.count()

    count_carts.short_description = "장바구니 개수"

    def count_orders(self, obj):
        return obj.orders.count()

    count_orders.short_description = "주문 개수"

    def count_reviews(self, obj):
        return obj.reviews.count()

    count_reviews.short_description = "리뷰 개수"


@admin.register(models.Social)
class SocialAdmin(admin.ModelAdmin):
    """Review Admin Definition"""

    list_display = ("id", "user", "kind")


@admin.register(models.Withdrawal)
class Withdrawal(admin.ModelAdmin):
    list_display = ("id", "user", "reasons", "reason_others", "created_at")
    list_filter = ('reasons',)
