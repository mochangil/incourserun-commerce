from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.CartListCreateView.as_view()),
    path('/<int:pk>', views.CartDetailUpdateDeleteView.as_view()),
]