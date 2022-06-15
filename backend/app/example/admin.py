from django.contrib import admin
from app.example.models import Example


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass
