from django.core.management.base import BaseCommand
from random import choice, sample
from tqdm.asyncio import tqdm
from tqdm import tqdm
from faker import Faker
from django.contrib.auth.models import User
import re
from transliterate import translit

from films.models import Film, Actor, Director, Genre, Review, Collection


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        genres = [ "Комедия",
                    "Драма",
                    "Ужасы",
                    "Триллер",
                    "Фэнтези",
                    "Научная фантастика",
                    "Романтика",
                    "Приключения",
                    "Документальное"
        ]

        for genre in genres:
            Genre.objects.create(name=genre)
        
        for _ in tqdm(list(range(1000))):
            Actor.objects.create(
                name=fake.name(),
                birth_date=fake.date_of_birth(),
                biography=fake.paragraph(nb_sentences=5)
            )

            Director.objects.create(
                name=fake.name(),
                birth_date=fake.date_of_birth(),
                biography=fake.paragraph(nb_sentences=5)
            )

            Genre.objects.create(
                name=fake.word()
            )

            
            
            fio = fake.name()
            fio_translited = translit(fio, 'ru', reversed=True).lower()
            fio_translited = re.sub("['-]", "", fio_translited)
            fio_translited = fio_translited.replace(" ", "_")
            print(fio_translited)

            user = User.objects.create_user(
                username=fio_translited,
                email=f"{fio_translited}@gmail.com",
                password="123"
            )

            user.profile.role = 2
            user.profile.save()

        for _ in tqdm(list(range(1000))):
            Film.objects.create(
                name = fake.sentence(nb_words=3),
                description = fake.paragraph(nb_sentences=5),
                rating = fake.random_int(min=1, max=10),
                genre=choice(list(Genre.objects.all())),
                actors=sample(list(Actor.objects.all()), k=3),
                directors=sample(list(Director.objects.all()), k=2)
            )

            for _ in tqdm(list(range(1000))):
                review = Review.objects.create(
                    review_text=fake.paragraph(nb_sentences=5),
                    rate=fake.random_int(min=1, max=10)
                )
                review.film = choice(list(Film.objects.all()))
                review.author = choice(list(User.objects.all()))
                review.save()


                collection = Collection.objects.create(
                    name=fake.sentence(nb_words=3),
                    price=fake.random_int(min=100, max=1000)
                )
                collection.films.set(sample(list(Film.objects.all()), k=5))
                collection.save()

                