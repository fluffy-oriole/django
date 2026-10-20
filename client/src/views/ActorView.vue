```vue
<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const actors = ref([]);
const loading = ref(false);
const actorToAdd = ref({});

async function fetchActors() {
    loading.value = true;
    try {
        const r = await axios.get('/api/actors/');
        actors.value = r.data;
    } finally {
        loading.value = false;
    }
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    fetchActors();
});

async function onActorAdd() {
    await axios.post('/api/actors/', {
        ...actorToAdd.value,
    });

    actorToAdd.value = {};
    await fetchActors();
}

async function onRemoveActor(actor) {
    await axios.delete(`/api/actors/${actor.id}/`);
    await fetchActors();
}
</script>

<template>
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
    grid-template-columns: 1fr auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>
```