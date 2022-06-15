from django.db import models


class Example(models.Model):
    title = models.CharField(verbose_name="타이틀", max_length=256)
    content = models.TextField(verbose_name="내용")
    is_active = models.BooleanField(verbose_name="노출 여부", default=True)

    class Meta:
        verbose_name = "Example"
        verbose_name_plural = verbose_name
