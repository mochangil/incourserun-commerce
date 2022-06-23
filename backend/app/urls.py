from django.urls import path, include

urlpatterns = [
    path("example", include("app.example.urls")),
    path("users", include("app.user.urls")),
    path("products", include("app.product.urls")),
    path("orders", include("app.order.urls")),
    path('reviews', include("app.review.urls"))
]
