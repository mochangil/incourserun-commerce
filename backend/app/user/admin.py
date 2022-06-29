from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin


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
        "created_at"
    )

@admin.register(models.Social)
class SocialAdmin(admin.ModelAdmin):

    """Review Admin Definition"""

    list_display = ("id", "user","kind")

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")
