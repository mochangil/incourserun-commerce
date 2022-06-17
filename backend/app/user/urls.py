from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('/social_login', views.UserSocialLoginView.as_view()),
    path('/login/kakao', views.kakao_login),
    path('/login/kakao/callback', views.kakao_callback),
]