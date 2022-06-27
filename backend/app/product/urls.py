from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('', views.ProductListCreateView.as_view()),
    path('/<int:pk>', views.ProductDetailUpdateDeleteView.as_view())
]