from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('', views.OrderListCreateView.as_view()),
    path('/<int:pk>', views.OrderDetailUpdateDeleteView.as_view()),
    path('/order-products/<int:pk>', views.OrderProductDetailUpdateView.as_view()),
    path('/payment_complete',views.payment_complete),
    # path('/payment_validation',views.PaymentValidationView.as_view())
    path('/iamport_webhook',views.payment_complete),
]