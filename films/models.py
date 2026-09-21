from django.db import models

class Film(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    rating = models.IntegerField("Рейтинг")
    release_date = models.DateField("Дата выхода")

    director = models.ForeignKey("Director", on_delete=models.CASCADE, verbose_name="Режиссер")
    actors = models.ManyToManyField("Actor", related_name="films")
    reviews = models.ForeignKey("Review", on_delete=models.CASCADE, verbose_name="Рецензия")

    def __str__(self) -> str:
        return self.name

class Genres(models.Model):
    name = models.TextField("Название")

class Review(models.Model):
    review_text = models.TextField("Текст рецензии")
    author = models.TextField("Автор")
    rate = models.IntegerField("Оценка")

class Director(models.Model):
    name = models.TextField("ФИО")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    biofraphy = models.TextField("Биография", null=True, blank=True)

class Actor(models.Model):
    name = models.TextField("ФИО")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    biography = models.TextField("Биография", null=True, blank=True)
