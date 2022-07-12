from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", related_name="reviews", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', verbose_name="상품", related_name="reviews", on_delete=models.CASCADE)
    order_product = models.OneToOneField('order.OrderProduct', verbose_name="주문-상품", related_name="review", on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="별점", validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.CharField(verbose_name="내용", max_length = 1000, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)

    class Meta:
        verbose_name = "리뷰"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Review({self.id}) - {self.user} - {self.product}'
 

class Photo(models.Model):
    review = models.ForeignKey('review.Review', verbose_name="리뷰", related_name="photos", on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="이미지", upload_to="review")

    class Meta:
        verbose_name = "리뷰 사진"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'Photo({self.id}) - {self.review.product} - {self.img}'
        
    def save(self, *args, **kwargs):
        if Photo.objects.filter(review=self.review).count() >= 3:
            raise ValidationError({'photoCount': '리뷰 하나에 사진은 3개까지만 등록 가능합니다.'})
        return super(Photo, self).save(*args, **kwargs)


class Reply(models.Model):
    review = models.OneToOneField('review.Review', verbose_name="리뷰", related_name="reply", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="내용", max_length = 1000)
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)

    class Meta:
        verbose_name = "리뷰 답글"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'Reply({self.id}) - {self.content}'