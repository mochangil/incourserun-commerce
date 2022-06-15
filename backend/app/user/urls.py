from django.urls import path

from app.user.views import UserSocialLoginView

urlpatterns = [
    path('/social_login', UserSocialLoginView.as_view()),
]