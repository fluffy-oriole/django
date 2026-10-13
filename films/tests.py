from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from films.models import Film, Genre, Review, Director, Actor, Collection


class FilmsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        actor = baker.make('films.Actor')
        director = baker.make('films.Director')
        genre = baker.make('films.Genre')
        film = baker.make('films.Film', genre=genre, actors=[actor], directors=[director])

        r = self.client.get('/api/films/')
        data = r.json()

        assert len(data) == 1
        assert data[0]['id'] == film.id
        assert data[0]['name'] == film.name
        assert data[0]['description'] == film.description
        assert data[0]['rating'] == film.rating
        assert data[0]['genre'] == genre.id
        assert data[0]['directors'] == [d.id for d in film.directors.all()]
        assert data[0]['actors'] == [a.id for a in film.actors.all()]

    def test_create_film(self):
        actor = baker.make('films.Actor')
        director = baker.make('films.Director')
        genre = baker.make('films.Genre')

        r = self.client.post('/api/films/', {
            'name': 'Test Film',
            'description': 'Test Description',
            'rating': 8.5,
            'genre': genre.id,
            'directors': [director.id],
            'actors': [actor.id],
        })
        assert r.status_code == 201

        film = Film.objects.get(id=r.json()['id'])
        assert film.name == 'Test Film'
        assert film.description == 'Test Description'
        assert film.rating == 8.5
        assert film.genre == genre
        assert list(film.directors.all()) == [director]
        assert list(film.actors.all()) == [actor]

    def test_delete_film(self):
        films = baker.make('films.Film', 3)
        film_id = films[0].id

        r = self.client.delete(f'/api/films/{film_id}/')
        assert r.status_code == 204
        assert not Film.objects.filter(id=film_id).exists()
        assert Film.objects.count() == 2

    def test_update_film(self):
        actor = baker.make('films.Actor')
        director = baker.make('films.Director')
        genre = baker.make('films.Genre')
        film = baker.make('films.Film', genre=genre, actors=[actor], directors=[director])

        r = self.client.put(f'/api/films/{film.id}/', {
            'name': 'Updated Film',
            'description': 'Updated Description',
            'rating': 9.0,
            'genre': genre.id,
            'directors': [director.id],
            'actors': [actor.id],
        })
        assert r.status_code == 200

        film.refresh_from_db()
        assert film.name == 'Updated Film'
        assert film.description == 'Updated Description'
        assert film.rating == 9.0
        assert film.genre == genre
        assert list(film.directors.all()) == [director]
        assert list(film.actors.all()) == [actor]


class GenreViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        genre = baker.make('films.Genre', name='Drama')

        r = self.client.get('/api/genres/')
        data = r.json()

        assert len(data) == 1
        assert data[0]['id'] == genre.id
        assert data[0]['name'] == genre.name

    def test_create_genre(self):
        r = self.client.post('/api/genres/', {'name': 'Comedy'})
        assert r.status_code == 201

        genre = Genre.objects.get(id=r.json()['id'])
        assert genre.name == 'Comedy'

    def test_delete_genre(self):
        genres = baker.make('films.Genre', 3)
        genre_id = genres[0].id

        r = self.client.delete(f'/api/genres/{genre_id}/')
        assert r.status_code == 204
        assert not Genre.objects.filter(id=genre_id).exists()
        assert Genre.objects.count() == 2

    def test_update_genre(self):
        genre = baker.make('films.Genre', name='Drama')

        r = self.client.put(f'/api/genres/{genre.id}/', {'name': 'Thriller'})
        assert r.status_code == 200

        genre.refresh_from_db()
        assert genre.name == 'Thriller'


class DirectorViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        director = baker.make('films.Director', name='Test Director', birth_date='1980-01-01', biography='Biography')

        r = self.client.get('/api/directors/')
        data = r.json()

        assert len(data) == 1
        assert data[0]['id'] == director.id
        assert data[0]['name'] == director.name
        assert data[0]['birth_date'] == '1980-01-01'
        assert data[0]['biography'] == 'Biography'

    def test_create_director(self):
        r = self.client.post('/api/directors/', {
            'name': 'Test Director',
            'birth_date': '1980-01-01',
            'biography': 'Biography'
        })
        assert r.status_code == 201

        director = Director.objects.get(id=r.json()['id'])
        assert director.name == 'Test Director'
        assert str(director.birth_date) == '1980-01-01'
        assert director.biography == 'Biography'

    def test_delete_director(self):
        directors = baker.make('films.Director', 3)
        director_id = directors[0].id

        r = self.client.delete(f'/api/directors/{director_id}/')
        assert r.status_code == 204
        assert not Director.objects.filter(id=director_id).exists()
        assert Director.objects.count() == 2

    def test_update_director(self):
        director = baker.make('films.Director')

        r = self.client.put(f'/api/directors/{director.id}/', {
            'name': 'Updated Director',
            'birth_date': '1990-05-10',
            'biography': 'Updated Biography'
        })
        assert r.status_code == 200

        director.refresh_from_db()
        assert director.name == 'Updated Director'
        assert str(director.birth_date) == '1990-05-10'
        assert director.biography == 'Updated Biography'


class ActorViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        actor = baker.make('films.Actor', name='Test Actor', birth_date='1985-03-12', biography='Biography')

        r = self.client.get('/api/actors/')
        data = r.json()

        assert len(data) == 1
        assert data[0]['id'] == actor.id
        assert data[0]['name'] == actor.name
        assert data[0]['birth_date'] == '1985-03-12'
        assert data[0]['biography'] == 'Biography'

    def test_create_actor(self):
        r = self.client.post('/api/actors/', {
            'name': 'Test Actor',
            'birth_date': '1985-03-12',
            'biography': 'Biography'
        })
        assert r.status_code == 201

        actor = Actor.objects.get(id=r.json()['id'])
        assert actor.name == 'Test Actor'
        assert str(actor.birth_date) == '1985-03-12'
        assert actor.biography == 'Biography'

    def test_delete_actor(self):
        actors = baker.make('films.Actor', 3)
        actor_id = actors[0].id

        r = self.client.delete(f'/api/actors/{actor_id}/')
        assert r.status_code == 204
        assert not Actor.objects.filter(id=actor_id).exists()
        assert Actor.objects.count() == 2

    def test_update_actor(self):
        actor = baker.make('films.Actor')

        r = self.client.put(f'/api/actors/{actor.id}/', {
            'name': 'Updated Actor',
            'birth_date': '1990-05-10',
            'biography': 'Updated Biography'
        })
        assert r.status_code == 200

        actor.refresh_from_db()
        assert actor.name == 'Updated Actor'
        assert str(actor.birth_date) == '1990-05-10'
        assert actor.biography == 'Updated Biography'


class ReviewViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        film = baker.make('films.Film')
        review = baker.make('films.Review', film=film, review_text='Good film', author='Test Author', rate=8)

        r = self.client.get('/api/reviews/')
        data = r.json()

        assert len(data) == 1
        assert data[0]['id'] == review.id
        assert data[0]['film'] == film.id
        assert data[0]['review_text'] == review.review_text
        assert data[0]['author'] == review.author
        assert data[0]['rate'] == review.rate

    def test_create_review(self):
        film = baker.make('films.Film')

        r = self.client.post('/api/reviews/', {
            'film': film.id,
            'review_text': 'Great film',
            'author': 'Test Author',
            'rate': 9
        })
        assert r.status_code == 201

        review = Review.objects.get(id=r.json()['id'])
        assert review.film == film
        assert review.review_text == 'Great film'
        assert review.author == 'Test Author'
        assert review.rate == 9

    def test_delete_review(self):
        reviews = baker.make('films.Review', 3)
        review_id = reviews[0].id

        r = self.client.delete(f'/api/reviews/{review_id}/')
        assert r.status_code == 204
        assert not Review.objects.filter(id=review_id).exists()
        assert Review.objects.count() == 2

    def test_update_review(self):
        film = baker.make('films.Film')
        review = baker.make('films.Review', film=film)

        r = self.client.put(f'/api/reviews/{review.id}/', {
            'film': film.id,
            'review_text': 'Updated Review',
            'author': 'Updated Author',
            'rate': 7
        })
        assert r.status_code == 200

        review.refresh_from_db()
        assert review.film == film
        assert review.review_text == 'Updated Review'
        assert review.author == 'Updated Author'
        assert review.rate == 7


class CollectionViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        films = baker.make('films.Film', 2)
        collection = baker.make('films.Collection', name='Test Collection', price=19.99, films=films)

        r = self.client.get('/api/collections/')
        data = r.json()

        assert len(data) == 1
        assert data[0]['id'] == collection.id
        assert data[0]['name'] == collection.name
        assert data[0]['price'] == collection.price
        assert data[0]['films'] == [film.id for film in collection.films.all()]

    def test_create_collection(self):
        films = baker.make('films.Film', 2)
        film_ids = [film.id for film in films]

        r = self.client.post('/api/collections/', {
            'name': 'Test Collection',
            'price': 19.99,
            'films': film_ids
        })
        assert r.status_code == 201

        collection = Collection.objects.get(id=r.json()['id'])
        assert collection.name == 'Test Collection'
        assert collection.price == 19.99
        assert list(collection.films.all()) == films

    def test_delete_collection(self):
        collections = baker.make('films.Collection', 3)
        collection_id = collections[0].id

        r = self.client.delete(f'/api/collections/{collection_id}/')
        assert r.status_code == 204
        assert not Collection.objects.filter(id=collection_id).exists()
        assert Collection.objects.count() == 2

    def test_update_collection(self):
        films = baker.make('films.Film', 2)
        collection = baker.make('films.Collection', name='Old Collection', price=10.0, films=films)

        new_films = baker.make('films.Film', 2)
        new_film_ids = [film.id for film in new_films]

        r = self.client.put(f'/api/collections/{collection.id}/', {
            'name': 'Updated Collection',
            'price': 25.0,
            'films': new_film_ids
        })
        assert r.status_code == 200

        collection.refresh_from_db()
        assert collection.name == 'Updated Collection'
        assert collection.price == 25.0
        assert list(collection.films.all()) == new_films