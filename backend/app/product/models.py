from django.db import models

# Create your models here.
class CategoryChoices(models.TextChoices):
    BATHNSHAMPOO = 'bathnshampoo', '바스&샴푸'
    OIL = 'oil', '오일'
    LOTION = 'lotion', '로션'
    CREAM = 'cream', '크림'
    POWDERLOTION = 'powderlotion', '파우더로션'

class Product(models.Model):
    name = models.CharField(verbose_name="상품명", max_length=100)
    category = models.CharField(verbose_name="분류", max_length=12, choices=CategoryChoices.choices)
    capacity = models.IntegerField(verbose_name="용량")
    price = models.IntegerField(verbose_name="가격")
    photo = models.CharField(verbose_name="상품이미지", max_length=1000)
    detail = models.CharField(verbose_name="상세이미지", max_length=1000)
    hashtags = models.ManyToManyField("Hashtag", related_name = "products", blank=True)
    created = models.DateTimeField(verbose_name="등록일시", auto_now_add=True)

    class Meta:
        verbose_name = "상품"
        verbose_name_plural = verbose_name
    
    def __str(self):
        return self.name

class Hashtag(models.Model):
    name = models.CharField(verbose_name="이름", max_length=20)

    class Meta:
        verbose_name = "해시태그"
        verbose_name_plural = verbose_name
    
    def __str(self):
        return self.name