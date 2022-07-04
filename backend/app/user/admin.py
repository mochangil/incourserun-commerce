from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = (
        ('Personal info', 
            {'fields': (
            "username",
            "password",
            "nickname",
            "email", 
            "is_active",
            "is_staff",
            "is_superuser",
            "is_register",
            "gender",
            "age",
            "zipcode",
            "address",
            "address_detail",
            "profile_img",
            )}
        ),
    )

    list_filter = UserAdmin.list_filter

    list_display = (
        "id",
        "username",
        "nickname",
        "email",
        "get_profile_img",
        "gender",
        "age",
        "zipcode",
        "address",
        "address_detail",
        "created_at",
        "count_carts",
        "count_orders",
        "count_reviews",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_register",
    )

    def get_profile_img(self, obj):
        url = obj.profile_img.url if obj.profile_img else ""
        return mark_safe(f'<div><a href="{url}">{obj.profile_img}</a><img width="100px" src="{url}" /></div>')
    get_profile_img.short_description = "프로필사진"
    
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

    list_display = ("id", "user","kind")

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")

@admin.register(models.Withdrawal)
class Withdrawal(admin.ModelAdmin):
    list_display = ("id","user")
