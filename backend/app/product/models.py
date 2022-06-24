from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class CategoryChoices(models.TextChoices):
    BATHNSHAMPOO = '바스 & 샴푸', '바스 & 샴푸'
    OIL = '오일', '오일'
    LOTION = '로션', '로션'
    CREAM = '크림', '크림'
    POWDERLOTION = '파우더로션', '파우더로션'

class Product(models.Model):
    name = models.CharField(verbose_name="상품명", max_length=100)
    category = models.CharField(verbose_name="분류", max_length=12, choices=CategoryChoices.choices)
    capacity = models.IntegerField(verbose_name="용량", validators=[MinValueValidator(1)])
    price = models.IntegerField(verbose_name="가격", validators=[MinValueValidator(0)])
    description = models.CharField(verbose_name="상품설명", max_length=1000, null=True, blank=True)
    product_img = models.ImageField(verbose_name="상품이미지", upload_to="product", null=True, blank=True)
    detail_img = models.ImageField(verbose_name="상세이미지", upload_to="detail", null=True, blank=True)
    hashtags = models.ManyToManyField("Hashtag", related_name = "products", blank=True)
    created = models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        verbose_name = "상품"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name

class Hashtag(models.Model):
    name = models.CharField(verbose_name="이름", max_length=20)

    class Meta:
        verbose_name = "해시태그"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name