from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey('user.User', related_name="carts", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name="carts", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="수량", validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = "장바구니"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product'),
        ]