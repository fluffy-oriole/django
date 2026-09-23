from django.db import models

class Film(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание")
    rating = models.FloatField("Рейтинг")
    release_date = models.DateField("Дата выхода")

    directors = models.ManyToManyField("Director", related_name="films")
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, null=True)
    actors = models.ManyToManyField("Actor", related_name="films")

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

    def __str__(self) -> str:
            return self.name

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"
