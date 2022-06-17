import requests
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from app.user.serializers import UserSocialLoginSerializer
from django.shortcuts import redirect
from django.conf import settings


class UserSocialLoginView(CreateAPIView):
    """
    유저 소셜로그인
    ---
    소셜로그인의 callback으로 전달받은 code와 state값으로 로그인 또는 회원가입을 합니다.
    """
    serializer_class = UserSocialLoginSerializer


def kakao_login(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = "http://127.0.0.1:8000/v1/user/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )
    
def kakao_callback(request):
    code = request.GET.get("code")
    redirect_uri = settings.KAKAO_REDIRECT_URL

    url = "http://127.0.0.1:8000/v1/user/social_login"
    data = {
        'code': code,
        'state':'kakao',
        'redirect_uri': redirect_uri,
    }
    response = requests.post(url=url, data=data)
    if not response.ok:
        raise ValidationError()
    return redirect("http://127.0.0.1:8000/v1/user")
