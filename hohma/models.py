from django.db import models

# Create your models here.
class hohma(models.Model):
    name = models.TextField("Название")
    group_name = models.TextField("Название группы")

    class Meta:
        verbose_name = "Хохма"
        verbose_name_plural = 'Хохмы'