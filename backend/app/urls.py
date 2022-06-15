from django.urls import path, include

urlpatterns = [
    path("example", include("app.example.urls")),
    path("user", include("app.user.urls")),
]
