from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('', views.OrderListCreateView.as_view()),
    path('/<int:pk>', views.OrderDetailUpdateDeleteView.as_view()),
    path('/order-products/<int:pk>', views.OrderProductDetailUpdateView.as_view()),
    path('/payment/complete',views.OrderPaymentView.as_view()),
    path('/payment/cancel', views.CancelCreateView.as_view()),
    path('/payment/complete',views.OrderPaymentView.as_view()),
]