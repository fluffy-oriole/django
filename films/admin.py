from django.contrib import admin
from films.models import Film, Genre, Review, Director, Actor

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ["name", "release_date", "rating", "genre"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["film", "author", "rate"]

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]