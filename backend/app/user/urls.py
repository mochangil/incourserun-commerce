from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . import views

app_name = "user"

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('/<int:pk>', views.UserDetailUpdateDeleteView.as_view()),
    path('/social_login', views.UserSocialLoginView.as_view()),
    path('/withdrawal',views.UserWithdrawalListCreateView.as_view()),
    path('/withdrawal/<int:pk>',views.UserWithdrawalUpdateDeleteView.as_view()),
    path('/token/', TokenObtainPairView.as_view()),
    path('/token/refresh', TokenRefreshView.as_view()),
    path('/login/kakao', views.kakao_login),
    path('/login/kakao/callback', views.kakao_callback),
]