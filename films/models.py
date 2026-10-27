from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    class Role(models.IntegerChoices):
        undefined = 0
        admin = 1
        user = 2

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    role = models.IntegerField("Роль", choices=Role, default=Role.undefined)

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Film(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    rating = models.FloatField("Рейтинг")

    directors = models.ManyToManyField("Director", related_name="films")
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, null=True)
    actors = models.ManyToManyField("Actor", related_name="films")

    picture = models.ImageField("Изображение", null=True, upload_to="films")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    name = models.TextField("Название")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Review(models.Model):
    film = models.ForeignKey("Film", on_delete=models.CASCADE, null=True)
    review_text = models.TextField("Текст рецензии")
    author = models.TextField("Автор")
    rate = models.IntegerField("Оценка")

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"

class Director(models.Model):
    name = models.TextField("ФИО")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    biography = models.TextField("Биография", null=True, blank=True)

    def __str__(self) -> str:
            return self.name

    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"

class Actor(models.Model):
    name = models.TextField("ФИО")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    biography = models.TextField("Биография", null=True, blank=True)

    picture = models.ImageField("Изображение", null=True, upload_to="actors")

    def __str__(self) -> str:
            return self.name

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"


class Collection(models.Model):
    name = models.TextField("Название")
    films = models.ManyToManyField("Film", related_name="collections")
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Коллекция фильмов"
        verbose_name_plural = "Коллекции фильмов"