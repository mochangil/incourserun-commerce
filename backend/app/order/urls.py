from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('', views.OrderListCreateView.as_view()),
    path('/<int:pk>', views.OrderDetailUpdateDeleteView.as_view()),
    path('/product', views.OrderProductListCreateView.as_view()),
    path('/product/<int:pk>', views.OrderProductDetailUpdateDeleteView.as_view())
]