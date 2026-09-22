from django.db import models

class Film(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    rating = models.IntegerField("Рейтинг")
    release_date = models.DateField("Дата выхода")

    director = models.ForeignKey("Director", on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    actors = models.ManyToManyField("Actor", related_name="films")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    name = models.TextField("Название")

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

    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"

class Actor(models.Model):
    name = models.TextField("ФИО")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    biography = models.TextField("Биография", null=True, blank=True)

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"
