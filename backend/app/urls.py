from django.urls import path, include

urlpatterns = [
    path("users", include("app.user.urls")),
    path("carts", include("app.cart.urls")),
    path("products", include("app.product.urls")),
    path("orders", include("app.order.urls")),
    path('reviews', include("app.review.urls"))
]
