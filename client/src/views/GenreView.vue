<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const genres = ref([]);
const loading = ref(false);
const genreToAdd = ref({});
const genreToEdit = ref({});

async function fetchGenres() {
    loading.value = true;
    try {
        const r = await axios.get('/api/genres/');
        genres.value = r.data;
    } finally {
        loading.value = false;
    }
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchGenres();
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

        <strong><div>Жанры</div></strong>

        <div
            v-for="genre in genres"
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