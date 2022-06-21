from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path('', views.ReviewListCreateView.as_view()),
    path('/<int:pk>', views.ReviewDetailUpdateDeleteView.as_view()),
    path('/photo', views.PhotoListCreateView.as_view()),
    path('/photo/<int:pk>', views.PhotoDetailUpdateDeleteView.as_view()),
    path('/reply', views.ReplyListCreateView.as_view()),
    path('/reply/<int:pk>', views.ReplyDetailUpdateDeleteView.as_view())
]