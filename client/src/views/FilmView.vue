<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import Cookies from 'js-cookie';
import axios from "axios";


const loading = ref(false);

const films = ref([]);
const filmToAdd = ref({ directors: [], actors: [] });
const filmToEdit = ref({ directors: [], actors: [] })

const genres = ref([]);
const actors = ref([]);
const directors = ref([]);

const filmPictureRef = ref();
const filmEditPictureRef = ref();

const filmAddImageUrl = ref();
const filmEditImageUrl = ref();

const showPictureModal = ref();

const filmImages = ref([]);
const filmImagesRef = ref();

const filmEditImages = ref([]);
const filmEditImagesRef = ref();

const users = ref([]);
const userIdTofilter = ref();

const countOfFilms = ref(0);
const avgRatingOfFilms = ref(0);
const minRatingOfFilms = ref(0);
const maxRatingOfFilms = ref(0);

const page = ref(0);
const pageItemsCount = ref(10);

const filteredFilms = computed(() => {
    return films.value.slice(
        page.value * pageItemsCount.value,
        (page.value + 1) * pageItemsCount.value
     );
})

const pagesCount = computed(() => {
    return Math.trunc(films.value.length / pageItemsCount.value + 1);
})

async function fetchFilmStats() {
    loading.value = true;
    const r = await axios.get('/api/films/stats/');
    console.log(r.data);
    countOfFilms.value = r.data.count;
    avgRatingOfFilms.value = r.data.avg;
    maxRatingOfFilms.value = r.data.max;
    minRatingOfFilms.value = r.data.min;
    console.log(countOfFilms.value, avgRatingOfFilms.value, minRatingOfFilms.value, maxRatingOfFilms.value);
    loading.value = false;
}

async function fetchUsers() {
    loading.value = true;
    const r = await axios.get('/api/users/');
    users.value = r.data;
    loading.value = false;
}

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
    genres.value = r.data;
    loading.value = false;
}

async function fetchFilms() {
    loading.value = true;
    const r = await axios.get('/api/films/', { params: { userId: userIdTofilter.value } });
    films.value = r.data;
    loading.value = false;
}


async function onLoadClick() {
    await fetchFilms();
    await fetchGenres();
    await fetchActors();
    await fetchDirectors();
    await fetchUsers();
    await fetchFilmStats();
}


onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    onLoadClick();
});


async function onFilmAdd() {
    const formData = new FormData();
    formData.append('picture', filmPictureRef.value.files[0]);

    formData.set('name', filmToAdd.value.name);
    formData.set('description', filmToAdd.value.description);
    formData.set('rating', filmToAdd.value.rating);
    formData.set('genre', filmToAdd.value.genre);

    for (const d of filmToAdd.value.directors) {
        formData.append('directors', d);
    }

    for (const a of filmToAdd.value.actors) {
        formData.append('actors', a);
    }

    const film = await axios.post('/api/films/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });

    for (const file of filmImages.value) {
        const imageFormData = new FormData();
        imageFormData.append('film', film.data.id);
        imageFormData.append('image', file);

        await axios.post('/api/film-images/', imageFormData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    }

    await fetchFilms();
}


async function onRemoveFilm(film) {
    await axios.delete(`/api/films/${film.id}/`);
    await fetchFilms();
}


async function onFilmEditClick(film) {
    filmToEdit.value = { ...film };
    filmEditImageUrl.value = film.picture;
}


async function onUpdateFilm() {
    const formData = new FormData();

    formData.set('name', filmToEdit.value.name);
    formData.set('description', filmToEdit.value.description);
    formData.set('rating', filmToEdit.value.rating);
    formData.set('genre', filmToEdit.value.genre);

    for (const d of filmToEdit.value.directors) {
        formData.append('directors', d);
    }

    for (const a of filmToEdit.value.actors) {
        formData.append('actors', a);
    }

    const newPicture = filmEditPictureRef.value?.files?.[0];
    if (newPicture) {
        formData.append('picture', newPicture);
    }

    await axios.put(`/api/films/${filmToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    if (filmEditImages.value.length) {
        for (const img of filmToEdit.value.images) {
            await axios.delete(`/api/film-images/${img.id}/`);
        }

        for (const file of filmEditImages.value) {
            const imageFormData = new FormData();
            imageFormData.append('film', filmToEdit.value.id);
            imageFormData.append('image', file);

            await axios.post('/api/film-images/', imageFormData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
        }
    }
    await fetchFilms();
}

async function filmsAddPictureChange() {
    filmAddImageUrl.value = URL.createObjectURL(filmPictureRef.value.files[0]);
}

async function filmEditPictureChange() {
    const file = filmEditPictureRef.value?.files?.[0];
    if (file) {
        filmEditImageUrl.value = URL.createObjectURL(file);
    }
}

async function filmEditImagesChange() {
    filmEditImages.value = Array.from(filmEditImagesRef.value.files);
}

async function showPictureModalChange(picture) {
    showPictureModal.value = picture
}

async function filmImagesChange() {
    filmImages.value = Array.from(filmImagesRef.value.files);
}

async function onFilterChange() {
    fetchFilms()
}

</script>
<template>
    <div class="modal fade" id="editFilmModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактировать фильм
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
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
                                <select class="form-select" v-model="filmToEdit.directors" multiple>
                                    <option :value="director.id" v-for="director in directors" :key="director.id">
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
                                <select class="form-select" v-model="filmToEdit.actors" multiple>
                                    <option :value="actor.id" v-for="actor in actors" :key="actor.id">
                                        {{ actor.name }}
                                    </option>
                                </select>
                                <label for="floatingInput">Актёры</label>
                            </div>
                        </div>
                    </div>
                    <div class="row" mt-3>
                        <div class="col-auto">
                            <input type="file" class="form-control" ref="filmEditPictureRef" @change="filmEditPictureChange"/>
                        </div>

                        <div class="col-auto">
                            <img :src="filmEditImageUrl" style="max-height: 60px;" alt="">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-auto">
                            <input type="file" class="form-control" ref="filmEditImagesRef" @change="filmEditImagesChange" multiple/>
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


    <div class="modal" tabindex="-1" id="showPictureModal">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
            </div>
            <div class="modal-body d-flex justify-content-center">
                <img :src="showPictureModal" style="max-height: 700px; max-width: 900px;">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            </div>
            </div>
        </div>
    </div>


    <div class="container">
        <div v-if="loading">Загрузка...</div>

        <strong><div>Добавить фильм</div></strong>
        <form @submit.prevent.stop="onFilmAdd">
        <div class="row mb-2">
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
        </div>
        <div class="row mb-2">
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
        </div>
        <div class="row mb-2">
            <div class="col-auto">
                <input type="file" class="form-control" ref="filmPictureRef" @change="filmsAddPictureChange"/>
            </div>

            <div class="col-auto">
                <input type="file" class="form-control" ref="filmImagesRef" @change="filmImagesChange" multiple/>
            </div>
            
            <div class="col-auto">
                <img :src="filmAddImageUrl" style="max-height: 60px;" alt="">
            </div>
            
            <div class="col-auto">
            <button class="btn btn-primary">
                Добавить
            </button>
            </div>
        </div>
        </form>
        <div>
            <div><strong>Статистика</strong></div>
            <div>Количество фильмов: {{ countOfFilms }}</div>
            <div>Средний рейтинг: {{ avgRatingOfFilms }}</div>
            <div>Максимальный рейтинг: {{ maxRatingOfFilms }}</div>
            <div>Минимальный рейтинг: {{ minRatingOfFilms }}</div>
        </div>
        
        <strong><div>Фильмы</div></strong>
        <div class="row">
            <select class="form-select" v-model="userIdTofilter" @change="onFilterChange">
                <option :value="null">Все пользователи</option>
                <option :value="user.id" v-for="user in users">{{ user.id }}</option>
            </select>
        </div>
        
        <div v-for="film in filteredFilms" :key="film.id" class="container" >
            <div class="show-block">
                {{ film.name }}
                <div v-show="film.picture" data-bs-toggle="modal" data-bs-target="#showPictureModal" @click="showPictureModalChange(film.picture)">
                    <img :src="film.picture" style="max-height: 60px;">
                </div>
                <button class="btn btn-success" @click="onFilmEditClick(film)" data-bs-toggle="modal" data-bs-target="#editFilmModal">
                    <i class="bi bi-pen-fill"></i>
                </button>
                
                <button class="btn btn-danger" @click="onRemoveFilm(film)">
                    <i class="bi bi-x"></i>
                </button>
            </div>
            <div style="width: 500px;">
                <div :id="`carouselExample${film.id}`" class="carousel slide">
                    <div class="carousel-inner">
                        <div class="carousel-item active">
                            <img class="d-block w-100" :src="film.images?.[0]?.image" :key="film.images?.[0]?.id">
                        </div>
                        
                        <div data-bs-toggle="modal"  class="carousel-item" v-for="img in film.images.slice(1)" :key="img.id">
                            <img class="d-block w-100" :src="img.image">
                        </div>
                    </div>
                    <button class="carousel-control-prev" type="button" :data-bs-target="`#carouselExample${film.id}`" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" :data-bs-target="`#carouselExample${film.id}`" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Next</span>
                    </button>
                </div>
            </div>
        </div>
        <nav aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
                <div v-if="page - 1 > 0">
                    <li class="page-item">
                        <a @click="page = page -1" class="page-link">Previous</a>
                    </li>
                </div>
                <li @click="page = page - 1" class="page-item" v-if="page - 1 > 0"><a class="page-link" >{{ page - 1 }}</a></li>
                <li class="page-item" v-if="page > 0"><a class="page-link" >{{ page }}</a></li>
                <li @click="page = page + 1" class="page-item" v-if="page + 1 < pagesCount"><a class="page-link" >{{ page + 1 }}</a></li>
                <li @click="page = page + 2" class="page-item" v-if="page + 2 < pagesCount"><a class="page-link" >{{ page + 2 }}</a></li>
                <li @click="page = page + 3" class="page-item" v-if="page + 3 < pagesCount"><a class="page-link" >{{ page + 3 }}</a></li>

                <div v-if="page < pagesCount">
                    <li class="page-item">
                        <a @click="page = page + 1" class="page-link" href="#">Next</a>
                    </li>
                </div>
            </ul>
        </nav>
    </div>
</template>

<style scoped>
.show-block {
    display: grid;
    grid-template-columns: 1fr auto auto auto;
    align-items: center;
    gap: 16px;
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid;
    border-radius: 8px;
}
</style>
