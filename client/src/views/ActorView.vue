<script setup>
import { ref, onBeforeMount } from 'vue';
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


async function fetchActors() {
    loading.value = true;
    const r = await axios.get('/api/actors/');
    actors.value = r.data;
    loading.value = false;
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchActors();
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

    <div class="container">
        <div v-if="loading">Загрузка...</div>

        <strong><div>Актёры</div></strong>

        <div
            v-for="actor in actors"
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

            <div v-show="actor.picture"><img :src="actor.picture" style="max-height: 60px;"></div>

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
