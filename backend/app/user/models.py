from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.core.validators import MinValueValidator


class UserManager(DjangoUserManager):
    def _create_user(self, username, password=None, **extra_fields):
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class GenderChoices(models.TextChoices):
    MALE = 'male','남성' 
    FEMALE = 'female', '여성'

class AgeChoices(models.TextChoices):
    TEEN = 'teen', '10대'
    TWENTY = 'twenty', '20대'
    THIRTY = 'thirty', '30대'
    FORTY = 'forty', '40대'
    FIFTY = 'fifty', '50대 이상'


class User(AbstractUser):
    first_name = None
    last_name = None

    nickname = models.CharField(verbose_name="닉네임", max_length=10)
    email = models.EmailField(verbose_name="이메일", unique=True)
    phone = models.CharField(verbose_name="휴대폰", max_length=11, null=True, blank=True)
    gender = models.CharField(verbose_name="성별", max_length=6, choices=GenderChoices.choices, null=True, blank=True)
    age = models.CharField(verbose_name="연령대", max_length=6, choices=AgeChoices.choices, null=True, blank=True)
    zipcode = models.CharField(verbose_name="우편번호", max_length=7, null=True, blank=True)
    address = models.CharField(verbose_name="주소", max_length=1000, null=True, blank=True)
    address_detail = models.CharField(verbose_name="상세주소", max_length=1000, null=True, blank=True)
    profile = models.ImageField(verbose_name="프로필사진", upload_to=None, null=True, blank=True)
    is_register = models.BooleanField(verbose_name="등록여부", default=False)
    created = models.DateTimeField(verbose_name="가입일시", auto_now_add=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        verbose_name = "유저"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class SocialKindChoices(models.TextChoices):
    KAKAO = 'kakao', '카카오'
    NAVER = 'naver', '네이버'
    FACEBOOK = 'facebook', '페이스북'
    GOOGLE = 'google', '구글'
    APPLE = 'apple', '애플'


class Social(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    kind = models.CharField(verbose_name='타입', max_length=16, choices=SocialKindChoices.choices)

    class Meta:
        verbose_name = '소셜'
        verbose_name_plural = verbose_name


class Cart(models.Model):
    user = models.ForeignKey('user.User', related_name="carts", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name="carts", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="수량", validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = "장바구니"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product'),
        ]