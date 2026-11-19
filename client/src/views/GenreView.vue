<script setup>
import { ref, computed, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const genres = ref([]);
const loading = ref(false);
const genreToAdd = ref({});
const genreToEdit = ref({});

const countOfGenres = ref(0);

const page = ref(0);
const pageItemsCount = ref(10);

const filteredGenres = computed(() => {
    return genres.value.slice(
        page.value * pageItemsCount.value,
        (page.value + 1) * pageItemsCount.value
     );
})

const pagesCount = computed(() => {
    return Math.trunc(genres.value.length / pageItemsCount.value + 1);
})

async function fetchStats() {
    const r = await axios.get('/api/genres/stats');
    console.log(r.data.count);
    countOfGenres.value = r.data.count;
}


async function fetchGenres() {
    loading.value = true;
    const r = await axios.get('/api/genres/');
    console.log(r.data);
    genres.value = r.data;
    loading.value = false;
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchGenres();
    fetchStats();
});

async function onGenreAdd() {
    await axios.post('/api/genres/', {
        ...genreToAdd.value,
    });

    genreToAdd.value = {};
    await fetchGenres();
}

async function onRemoveGenre(genre) {
    await axios.delete(`/api/genres/${genre.id}/`);
    await fetchGenres();
}

function onGenreEditClick(genre) {
    genreToEdit.value = { ...genre };
}

async function onUpdateGenre() {
    await axios.put(`/api/genres/${genreToEdit.value.id}/`, {
        ...genreToEdit.value,
    });

    await fetchGenres();
}
</script>

<template>
    <div class="container">
        <div v-if="loading">Загрузка...</div>

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
                        <label>Название</label>
                    </div>
                </div>

                <div class="col-auto">
                    <button type="submit" class="btn btn-primary">
                        Добавить
                    </button>
                </div>
            </div>
        </form>

        <div>
            <div><strong>Статистика</strong></div>
            <div>Количество жанров: {{ countOfGenres }}</div>
        </div>

        <strong><div>Жанры</div></strong>

        <div
            v-for="genre in filteredGenres"
            :key="genre.id"
            class="show-block"
        >
            {{ genre.name }}

            <button
                class="btn btn-success"
                @click="onGenreEditClick(genre)"
                data-bs-toggle="modal"
                data-bs-target="#editGenreModal"
            >
                <i class="bi bi-pen-fill"></i>
            </button>

            <button
                class="btn btn-danger"
                @click="onRemoveGenre(genre)"
            >
                <i class="bi bi-x"></i>
            </button>
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

        

        <div
            class="modal fade"
            id="editGenreModal"
            tabindex="-1"
            aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Редактировать жанр</h5>

                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Закрыть"
                        ></button>
                    </div>

                    <div class="modal-body">
                        <div class="form-floating">
                            <input
                                type="text"
                                class="form-control"
                                v-model="genreToEdit.name"
                                required
                            />
                            <label>Название</label>
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
                            type="button"
                            class="btn btn-primary"
                            data-bs-dismiss="modal"
                            @click="onUpdateGenre"
                        >
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>
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