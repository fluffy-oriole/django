<script setup>
import { ref, computed, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const directors = ref([]);
const loading = ref(false);
const directorToAdd = ref({});
const directorToEdit = ref({});
const users = ref([]);
const userIdTofilter = ref();


const countOfDirectors = ref(0);
const avgBirthYearOfDirectors = ref(0);
const maxBirthYearOfDirectors = ref(0);
const minBirthYearOfDirectors = ref(0);

const page = ref(0);
const pageItemsCount = ref(10);

const filteredDirectors = computed(() => {
    return directors.value.slice(
        page.value * pageItemsCount.value,
        (page.value + 1) * pageItemsCount.value
     );
})

const pagesCount = computed(() => {
    return Math.trunc(directors.value.length / pageItemsCount.value + 1);
})

async function fetchDirectors() {
    loading.value = true;
    try {
        const r = await axios.get('/api/directors/', { params: { userId: userIdTofilter.value } });
        directors.value = r.data;
    } finally {
        loading.value = false;
    }
}

async function fetchUsers() {
    loading.value = true;
    const r = await axios.get('/api/users/');
    users.value = r.data;
    loading.value = false;
}

async function fetchStats() {
    const r = await axios.get('/api/directors/stats');
    countOfDirectors.value = r.data.count;
    avgBirthYearOfDirectors.value = r.data.avg;
    maxBirthYearOfDirectors.value = r.data.max;
    minBirthYearOfDirectors.value = r.data.min;
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchDirectors();
    fetchUsers();
    fetchStats();
});

async function onDirectorAdd() {
    await axios.post('/api/directors/', {
        ...directorToAdd.value,
    });

    directorToAdd.value = {};
    await fetchDirectors();
    await fetchStats();
}

async function onRemoveDirector(director) {
    await axios.delete(`/api/directors/${director.id}/`);
    await fetchDirectors();
    await fetchStats();
}

async function onDirectorEditClick(director) {
    directorToEdit.value = { ...director };
}

async function onUpdateDirector() {
    await axios.put(`/api/directors/${directorToEdit.value.id}/`, {
    ...directorToEdit.value,
    });
    await fetchDirectors();
    await fetchStats();
}
async function onFilterChange() {
    fetchDirectors()
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

        <div>
            <div><strong>Статистика</strong></div>
            <div>Количество режиссёров: {{ countOfDirectors }}</div>
            <div>Средний год рождения: {{ avgBirthYearOfDirectors }}</div>
            <div>Максимальный год рождения: {{ maxBirthYearOfDirectors }}</div>
            <div>Минимальный год рождения: {{ minBirthYearOfDirectors }}</div>
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

        <strong><div>Режиссёры</div></strong>

        <div class="row">
            <select class="form-select" v-model="userIdTofilter" @change="onFilterChange">
                <option :value="null">Все пользователи</option>
                <option :value="user.id" v-for="user in users">{{ user.username }}</option>
            </select>
        </div>

        <div
            v-for="director in filteredDirectors"
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