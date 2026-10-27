<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const directors = ref([]);
const loading = ref(false);
const directorToAdd = ref({});
const directorToEdit = ref({});

async function fetchDirectors() {
    loading.value = true;
    try {
        const r = await axios.get('/api/directors/');
        directors.value = r.data;
    } finally {
        loading.value = false;
    }
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchDirectors();
});

async function onDirectorAdd() {
    await axios.post('/api/directors/', {
        ...directorToAdd.value,
    });

    directorToAdd.value = {};
    await fetchDirectors();
}

async function onRemoveDirector(director) {
    await axios.delete(`/api/directors/${director.id}/`);
    await fetchDirectors();
}

async function onDirectorEditClick(director) {
    directorToEdit.value = { ...director };
}

async function onUpdateDirector() {
    await axios.put(`/api/directors/${directorToEdit.value.id}/`, {
    ...directorToEdit.value,
    });
    await fetchDirectors();
}
</script>

<template>
    <div class="modal fade" id="editDirectorModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">
                        редактировать режиссёра
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
                                    v-model="directorToEdit.name"
                                />
                                <label>ФИО</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <input
                                    type="date"
                                    class="form-control"
                                    v-model="directorToEdit.birth_date"
                                />
                                <label>Дата рождения</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <textarea
                                    class="form-control"
                                    v-model="directorToEdit.biography"
                                ></textarea>
                                <label>Биография</label>
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
                        @click="onUpdateDirector"
                    >
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div v-if="loading">Загрузка...</div>

        <strong><div>Режиссёры</div></strong>

        <div
            v-for="director in directors"
            :key="director.id"
            class="show-block"
        >
            <div>
                <strong>{{ director.name }}</strong>
                <div v-if="director.birth_date">
                    Дата рождения: {{ director.birth_date }}
                </div>
                <div v-if="director.biography">
                    {{ director.biography }}
                </div>
            </div>

            <button
                class="btn btn-success"
                @click="onDirectorEditClick(director)"
                data-bs-toggle="modal"
                data-bs-target="#editDirectorModal"
            >
                <i class="bi bi-pen-fill"></i>
            </button>

            <button
                class="btn btn-danger"
                @click="onRemoveDirector(director)"
            >
                <i class="bi bi-x"></i>
            </button>
        </div>

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
                    <button type="submit" class="btn btn-primary">
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