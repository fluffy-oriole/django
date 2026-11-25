<script setup>
import { ref, computed, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const actors = ref([]);
const loading = ref(false);
const actorToAdd = ref({});
const actorToEdit = ref({});
const actorsPictureRef = ref();
const actorAddImageUrl = ref();
const actorEditImageRef = ref();
const actorEditImageUrl = ref();
const showPictureModal = ref();
const users = ref([]);
const userIdTofilter = ref();

const countOfActors = ref(0); 
const avgBirthYearOfActors = ref(0);
const maxBirthYearOfActors = ref(0);
const minBirthYearOfActors = ref(0);

const page = ref(0);
const pageItemsCount = ref(10);

const filteredActors = computed(() => {
    return actors.value.slice(
        page.value * pageItemsCount.value,
        (page.value + 1) * pageItemsCount.value
     );
})

const pagesCount = computed(() => {
    return Math.trunc(actors.value.length / pageItemsCount.value + 1);
})


async function fetchActors() {
    loading.value = true;
    const r = await axios.get('/api/actors/', { params: { userId: userIdTofilter.value } });
    actors.value = r.data;
    loading.value = false;
}

async function fetchUsers() {
    loading.value = true;
    const r = await axios.get('/api/users/');
    users.value = r.data;
    loading.value = false;
}

async function fetchStats() {
    const r = await axios.get('/api/actors/stats');
    countOfActors.value = r.data.count;
    avgBirthYearOfActors.value = r.data.avg;
    maxBirthYearOfActors.value = r.data.max;
    minBirthYearOfActors.value = r.data.min;
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchActors();
    fetchUsers();
    fetchStats();
});

async function onActorAdd() {
    const formData = new FormData();

    formData.append('picture', actorsPictureRef.value.files[0]);
    formData.set('name', actorToAdd.value.name);
    formData.set('birth_date', actorToAdd.value.birth_date);
    formData.set('biography', actorToAdd.value.biography);

    await axios.post('/api/actors/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    await fetchActors();
    await fetchStats();
}

async function onActorEditClick(actor) {
    actorToEdit.value = { ...actor };
}

async function onUpdateActor() {
    const formData = new FormData();

    formData.set('name', actorToEdit.value.name);
    formData.set('birth_date', actorToEdit.value.birth_date || '');
    formData.set('biography', actorToEdit.value.biography || '');

    formData.append('picture', actorEditImageRef.value.files[0]);

    await axios.put(
        `/api/actors/${actorToEdit.value.id}/`, formData,  {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });

    await fetchActors();
    await fetchStats();
}

async function actorAddPictureChange() {
    actorAddImageUrl.value = URL.createObjectURL(actorsPictureRef.value.files[0]);
}

async function actorEditPictureChange() {
    actorEditImageUrl.value = URL.createObjectURL(actorEditImageRef.value.files[0]);
}


async function onRemoveActor(actor) {
    await axios.delete(`/api/actors/${actor.id}/`);
    await fetchActors();
    await fetchStats();
}


async function showPictureModalChange(picture) {
    showPictureModal.value = picture;
}

async function onFilterChange() {
    fetchActors()
}
</script>

<template>
    <div class="modal fade" id="editActorModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Редактировать актёра</h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Закрыть"
                    ></button>
                </div>

                <div class="modal-body">
                    <div class="form-floating mb-3">
                        <input
                            type="text"
                            class="form-control"
                            v-model="actorToEdit.name"
                            required
                        />
                        <label>ФИО</label>
                    </div>

                    <div class="form-floating mb-3">
                        <input
                            type="date"
                            class="form-control"
                            v-model="actorToEdit.birth_date"
                        />
                        <label>Дата рождения</label>
                    </div>

                    <div class="form-floating mb-3">
                        <textarea
                            class="form-control"
                            v-model="actorToEdit.biography"
                        ></textarea>
                        <label>Биография</label>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Новая фотография</label>
                        <input type="file" class="form-control" ref="actorEditImageRef" @change="actorEditPictureChange"/>
                    </div>

                    <div class="col-auto">
                        <img :src="actorEditImageUrl" style="max-height: 60px;" alt="">
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
                        @click="onUpdateActor"
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

        <div>
            <div><strong>Статистика</strong></div>
            <div>Количество актёров: {{ countOfActors }}</div>
            <div>Средний год рождения: {{ avgBirthYearOfActors }}</div>
            <div>Максимальный год рождения: {{ maxBirthYearOfActors }}</div>
            <div>Минимальный год рождения: {{ minBirthYearOfActors }}</div>
        </div>

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
                    <input :src="actorAddImageUrl" type="file" class="form-control" ref="actorsPictureRef" @change="actorAddPictureChange">
                </div>

                <div class="col-auto">
                    <img :src="actorAddImageUrl" style="max-height: 60px;" alt="">
                </div>


                <div class="col-auto">
                    <button type="submit" class="btn btn-primary">
                        Добавить
                    </button>
                </div>
            </div>
        </form>

        <strong><div>Актёры</div></strong>

        <div class="row">
            <select class="form-select" v-model="userIdTofilter" @change="onFilterChange">
                <option :value="null">Все пользователи</option>
                <option :value="user.id" v-for="user in users">{{ user.username }}</option>
            </select>
        </div>

        <div
            v-for="actor in filteredActors"
            :key="actor.id"
            class="show-block"
        >
            <div>
                <strong>{{ actor.name }}</strong>

                <div v-if="actor.birth_date">
                    Дата рождения: {{ actor.birth_date }}
                </div>

                <div v-if="actor.biography">
                    {{ actor.biography }}
                </div>
            </div>

            <div v-show="actor.picture" @click="showPictureModalChange(actor.picture)"  data-bs-toggle="modal" data-bs-target="#showPictureModal"><img :src="actor.picture" style="max-height: 60px;"></div>

            <button
                class="btn btn-success"
                @click="onActorEditClick(actor)"
                data-bs-toggle="modal"
                data-bs-target="#editActorModal"
            >
                <i class="bi bi-pen-fill"></i>
            </button>

            <button
                class="btn btn-danger"
                @click="onRemoveActor(actor)"
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
    grid-template-columns: 1fr auto auto auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>
