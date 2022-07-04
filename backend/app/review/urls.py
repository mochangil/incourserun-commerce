from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path('', views.ReviewListCreateView.as_view()),
    path('/<int:pk>', views.ReviewDetailUpdateDeleteView.as_view()),
    path('/photos', views.PhotoListCreateView.as_view()),
    path('/photos/<int:pk>', views.PhotoDetailUpdateDeleteView.as_view()),
]