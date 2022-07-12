from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('/<int:pk>', views.ProductDetailView.as_view())
]