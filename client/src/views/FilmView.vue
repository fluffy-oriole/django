<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from "axios";

const films = ref([]);
const loading = ref(false);
const filmToAdd = ref({});
const filmToEdit = ref({})
const genres = ref([]);
const actors = ref([]);
const directors = ref([]);

async function fetchDirectors() {
    loading.value = true;
    const r = await axios.get('/api/directors/');
    directors.value = r.data;
    loading.value = false;
}

async function fetchActors() {
    loading.value = true;
    const r = await axios.get('/api/actors/');
    actors.value = r.data;
    loading.value = false;
}

async function fetchGenres() {
    loading.value = true;
    const r = await axios.get('/api/genres/');
    console.log(r.data);
    genres.value = r.data;
    loading.value = false;
}

async function fetchFilms() {
    loading.value = true;
    const r = await axios.get("/api/films/");
    console.log(r.data);
    films.value = r.data;
    loading.value = false;
}


async function onLoadClick() {
    await fetchFilms();
    await fetchGenres();
    await fetchActors();
    await fetchDirectors();
}


onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    onLoadClick();
});


async function onFilmAdd() {
    const formData = new FormData();
    const file = filmsPictureRef.value?.files?.[0];

    if (file) {
        formData.append('picture', file);
    }

    formData.set('name', filmToAdd.value.name);
    formData.set('description', filmToAdd.value.description);
    formData.set('rating', filmToAdd.value.rating);
    formData.set('genre', filmToAdd.value.genre);

    const directorsId = [];
    for (const d of filmToAdd.value.directors) {
        formData.append('directors', d);
    }

    const actorsId = [];
    for (const a of filmToAdd.value.actors) {
        formData.append('actors', a);
    }

    await axios.post('/api/films/', formData);
    await fetchFilms();
}


async function onRemoveFilm(film) {
    await axios.delete(`/api/films/${film.id}/`);
    await fetchFilms();
}


async function onFilmEditClick(film) {
    filmToEdit.value = { ...film };
}


async function onUpdateFilm() {
    await axios.put(`/api/films/${filmToEdit.value.id}/`, {
    ...filmToEdit.value,
    });
    await fetchFilms();
}


</script>
<template>
    <div class="modal fade" id="editFilmModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        редактировать фильм
                    </h1>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col">
                            <div class="form-floating">
                                <input
                                    type="text"
                                    class="form-control"
                                    v-model="filmToEdit.name"
                                />
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="filmToEdit.genre">
                                    <option :value="g.id" v-for="g in genres" :key="g.id">
                                        {{ g.name }}
                                    </option>
                                </select>
                                <label for="floatingInput">Жанр</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <textarea
                                    class="form-control"
                                    v-model="filmToEdit.description"
                                ></textarea>
                                <label for="floatingInput">Описание</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <input
                                    type="number"
                                    class="form-control"
                                    v-model.number="filmToEdit.rating"
                                />
                                <label for="floatingInput">Рейтинг</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <select
                                    class="form-select"
                                    v-model="filmToEdit.directors"
                                    multiple
                                >
                                    <option
                                        :value="director.id"
                                        v-for="director in directors"
                                        :key="director.id"
                                    >
                                        {{ director.name }}
                                    </option>
                                </select>
                                <label for="floatingInput">Режиссёры</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <select
                                    class="form-select"
                                    v-model="filmToEdit.actors"
                                    multiple
                                >
                                    <option
                                        :value="actor.id"
                                        v-for="actor in actors"
                                        :key="actor.id"
                                    >
                                        {{ actor.name }}
                                    </option>
                                </select>
                                <label for="floatingInput">Актёры</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                    >
                        Закрыть
                    </button>
                    <button
                        data-bs-dismiss="modal"
                        type="button"
                        class="btn btn-primary"
                        @click="onUpdateFilm"
                    >
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>


    <div class="container">
        <div v-if="loading">Загрузка...</div>

        <strong><div>Фильмы</div></strong>
        <div v-for="film in films" :key="film.id" class="show-block">
            {{ film.name }}
            <button
                class="btn btn-success"
                @click="onFilmEditClick(film)"
                data-bs-toggle="modal"
                data-bs-target="#editFilmModal"
            >
                <i class="bi bi-pen-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveFilm(film)">
                <i class="bi bi-x"></i>
            </button>
        </div>

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
                    <select class="form-select" v-model="filmToAdd.actors" multiple required>
                        <option :value="actor.id" v-for="actor in actors">{{ actor.name }}</option>
                    </select>
                    <label for="floatingInput">Актёр</label>
                </div>
            </div>
            <!--
            <div class="col-auto">
                <input type="file" class="form-control" ref="filmsPictureRef">
            </div>
            -->


            <div class="col-auto">
            <button class="btn btn-primary">
                Добавить
            </button>
            </div>
        </div>
        </form>
    </div>
</template>

<style scoped>
.show-block {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>
