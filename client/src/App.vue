<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from "axios";

const films = ref([]);
const genres = ref([]);
const reviews = ref([]);
const directors = ref([]);
const actors = ref([]);
const collections = ref([]);

const loading = ref(false);

async function fetchFilms() {
    loading.value = true;
    const r = await axios.get("/api/films/");
    console.log(r.data);
    films.value = r.data;
    loading.value = false;
}

async function fetchGenres() {
    loading.value = true;
    const r = await axios.get("/api/genres/");
    console.log(r.data);
    genres.value = r.data;
    loading.value = false;
}

async function fetchReviews() {
    loading.value = true;
    const r = await axios.get("/api/reviews/");
    console.log(r.data);
    reviews.value = r.data;
    loading.value = false;
}

async function fetchDirectors() {
    loading.value = true;
    const r = await axios.get("/api/directors/");
    console.log(r.data);
    directors.value = r.data;
    loading.value = false;
}

async function fetchActors() {
    loading.value = true;
    const r = await axios.get("/api/actors/");
    console.log(r.data);
    actors.value = r.data;
    loading.value = false;
}

async function fetchCollections() {
    loading.value = true;
    const r = await axios.get("/api/collections/");
    console.log(r.data);
    collections.value = r.data;
    loading.value = false;
}

async function onLoadClick() {
    await fetchFilms();
    await fetchGenres();
    await fetchReviews();
    await fetchDirectors();
    await fetchActors();
    await fetchCollections();
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    onLoadClick();
});


const filmToAdd = ref({});
const genreToAdd = ref({});
const reviewToAdd = ref({});
const directorToAdd = ref({});
const actorToAdd = ref({});
const collectionToAdd = ref({});

async function onFilmAdd() {
  await axios.post("/api/films/", {
    ...filmToAdd.value,
  });
  await fetchFilms();
}

async function onGenreAdd() {
  await axios.post("/api/genres/", {
    ...genreToAdd.value,
  });
  await fetchGenres();
}

async function onReviewAdd() {
  await axios.post("/api/reviews/", {
    ...reviewToAdd.value,
  });
  await fetchReviews();
}

async function onDirectorAdd() {
  await axios.post("/api/directors/", {
    ...directorToAdd.value,
  });
  await fetchDirectors();
}

async function onActorAdd() {
  await axios.post("/api/actors/", {
    ...actorToAdd.value,
  });
  await fetchActors();
}

async function onCollectionAdd() {
  await axios.post("/api/collections/", {
    ...collectionToAdd.value,
  });
  await fetchCollections();
}

async function onRemoveFilm(film) {
  await axios.delete(`/api/films/${film.id}/`);
  await fetchFilms();
}

async function onRemoveGenre(genre) {
  await axios.delete(`/api/genres/${genre.id}/`);
  await fetchGenres();
}

async function onRemoveReview(review) {
  await axios.delete(`/api/reviews/${review.id}/`);
  await fetchReviews();
}

async function onRemoveDirector(director) {
  await axios.delete(`/api/directors/${director.id}/`);
  await fetchDirectors();
}

async function onRemoveActor(actor) {
  await axios.delete(`/api/actors/${actor.id}/`);
  await fetchActors();
}

async function onRemoveCollection(collection) {
  await axios.delete(`/api/collections/${collection.id}/`);
  await fetchCollections();
}

</script>

<template>
    <div v-if="loading">Загрузка...:/</div>

    <strong><div>Фильмы</div></strong>
    <div v-for="film in films" :key="film.id">
        {{ film.name }}
    </div>

    <strong><div>Жанры</div></strong>
    <div v-for="genre in genres" :key="genre.id">
        {{ genre.name }}
    </div>

    <strong><div>Рецензии</div></strong>
    <div v-for="review in reviews" :key="review.id">
        {{ review.film.name }}: {{ review.text }}
    </div>

    <strong><div>Режиссёры</div></strong>
    <div v-for="director in directors" :key="director.id">
        {{ director.name }}
    </div>

    <strong><div>Актёры</div></strong>
    <div v-for="actor in actors" :key="actor.id">
        {{ actor.name }}
    </div>

    <strong><div>Коллекции</div></strong>
    <div v-for="collection in collections" :key="collection.id">
        {{ collection.name }}
    </div>
    <button @click="onLoadClick" :disabled="loading">Загрузить данные</button>

    <strong><div>Добавить фильм</div></strong>
    <form @submit.prevent.stop="onFilmAdd">
    <div class="row">
        <div class="col">
            <div class="form-floating">
                <input
                type="text"
                class="form-control"
                v-model="filmToAdd.name"
                required
                />
                <label for="floatingInput">Название</label>
            </div>
        </div>
        <div class="col">
            <div class="form-floating">
                <input
                type="text"
                class="form-control"
                v-model="filmToAdd.description"
                required
                />
                <label for="floatingInput">Описание</label>
            </div>
        </div>
        <div class="col">
            <div class="form-floating">
                <input
                type="number"
                class="form-control"
                v-model="filmToAdd.rating"
                required
                />
                <label for="floatingInput">Рейтинг</label>
            </div>
        </div>
        <div class="col-auto">
            <div class="form-floating">
                <select class="form-select" v-model="filmToAdd.genre" required>
                    <option :value="genre.id" v-for="genre in genres">{{ genre.name }}</option>
                </select>
                <label for="floatingInput">Жанр</label>
            </div>
        </div>
        <div class="col-auto">
            <div class="form-floating">
                <select class="form-select" v-model="filmToAdd.directors" multiple required>
                    <option :value="director.id" v-for="director in directors">{{ director.name }}</option>
                </select>
                <label for="floatingInput">Режиссёр</label>
            </div>
        </div>
        <div class="col-auto">
            <div class="form-floating">
                <select class="form-select" v-model="filmToAdd.actors" required>
                    <option :value="actor.id" v-for="actor in actors">{{ actor.name }}</option>
                </select>
                <label for="floatingInput">Актёр</label>
            </div>
        </div>
        <div class="col-auto">
        <button class="btn btn-primary">
            Добавить
        </button>
        </div>
    </div>
    </form>

    <strong><div>Добавить жанр</div></strong>
    <form @submit.prevent.stop="onGenreAdd">
    <div class="row">
        <div class="col">
            <div class="form-floating">
                <input
                type="text"
                class="form-control"
                v-model="genreToAdd.name"
                required
                />
                <label for="floatingInput">Название</label>
            </div>
        </div>
        <div class="col-auto">
            <button class="btn btn-primary">
                Добавить
            </button>
        </div>       
    </div>
    </form>

    <strong><div>Добавить рецензию</div></strong>
    <form @submit.prevent.stop="onReviewAdd">
        <div class="row">
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="reviewToAdd.film" required>
                        <option :value="film.id" v-for="film in films" :key="film.id">
                            {{ film.name }}
                        </option>
                    </select>
                    <label>Фильм</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <textarea
                        class="form-control"
                        v-model="reviewToAdd.review_text"
                        required
                    ></textarea>
                    <label>Текст рецензии</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <input
                        type="text"
                        class="form-control"
                        v-model="reviewToAdd.author"
                        required
                    />
                    <label>Автор</label>
                </div>
            </div>

            <div class="col-auto">
                <div class="form-floating">
                    <input
                        type="number"
                        class="form-control"
                        v-model.number="reviewToAdd.rate"
                        required
                    />
                    <label>Оценка</label>
                </div>
            </div>

            <div class="col-auto">
                <button class="btn btn-primary">Добавить</button>
            </div>
        </div>
    </form>
    <strong><div>Добавить режиссёра</div></strong>
    <form @submit.prevent.stop="onDirectorAdd">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input
                        type="text"
                        class="form-control"
                        v-model="directorToAdd.name"
                        required
                    />
                    <label>ФИО</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <input
                        type="date"
                        class="form-control"
                        v-model="directorToAdd.birth_date"
                    />
                    <label>Дата рождения</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <textarea
                        class="form-control"
                        v-model="directorToAdd.biography"
                    ></textarea>
                    <label>Биография</label>
                </div>
            </div>

            <div class="col-auto">
                <button class="btn btn-primary">Добавить</button>
            </div>
        </div>
    </form>

    <strong><div>Добавить актёра</div></strong>
    <form @submit.prevent.stop="onActorAdd">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input
                        type="text"
                        class="form-control"
                        v-model="actorToAdd.name"
                        required
                    />
                    <label>ФИО</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <input
                        type="date"
                        class="form-control"
                        v-model="actorToAdd.birth_date"
                    />
                    <label>Дата рождения</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <textarea
                        class="form-control"
                        v-model="actorToAdd.biography"
                    ></textarea>
                    <label>Биография</label>
                </div>
            </div>

            <div class="col-auto">
                <button class="btn btn-primary">Добавить</button>
            </div>
        </div>
    </form>

    <strong><div>Добавить коллекцию</div></strong>
    <form @submit.prevent.stop="onCollectionAdd">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input
                        type="text"
                        class="form-control"
                        v-model="collectionToAdd.name"
                        required
                    />
                    <label>Название коллекции</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <select
                        class="form-select"
                        v-model="collectionToAdd.films"
                        multiple
                        required
                    >
                        <option
                            :value="film.id"
                            v-for="film in films"
                            :key="film.id"
                        >
                            {{ film.name }}
                        </option>
                    </select>
                    <label>Фильмы</label>
                </div>
            </div>

            <div class="col">
                <div class="form-floating">
                    <input
                        type="number"
                        step="0.01"
                        class="form-control"
                        v-model.number="collectionToAdd.price"
                        required
                    />
                    <label>Цена</label>
                </div>
            </div>

            <div class="col-auto">
                <button class="btn btn-primary">Добавить</button>
            </div>
        </div>
    </form>
</template>

<style scoped>
</style>
