from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('', views.ProductListCreateView.as_view()),
    path('/<int:pk>', views.ProductDetailUpdateDeleteView.as_view()),
    path('/hashtag', views.HashtagListCreateView.as_view()),
    path('/hashtag/<int:pk>', views.HashtagDetailUpdateDeleteView.as_view())
]