```vue
<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const collections = ref([]);
const films = ref([]);
const loading = ref(false);
const collectionToAdd = ref({});

async function fetchCollections() {
    loading.value = true;
    try {
        const r = await axios.get('/api/collections/');
        collections.value = r.data;
    } finally {
        loading.value = false;
    }
}

async function fetchFilms() {
    const r = await axios.get('/api/films/');
    films.value = r.data;
}

async function onLoadClick() {
    await Promise.all([
        fetchCollections(),
        fetchFilms()
    ]);
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    onLoadClick();
});

async function onCollectionAdd() {
    await axios.post('/api/collections/', {
        ...collectionToAdd.value,
    });

    collectionToAdd.value = {};
    await fetchCollections();
}

async function onRemoveCollection(collection) {
    await axios.delete(`/api/collections/${collection.id}/`);
    await fetchCollections();
}
</script>

<template>
    <div class="container">
        <div v-if="loading">Загрузка...</div>

        <strong><div>Коллекции</div></strong>

        <div
            v-for="collection in collections"
            :key="collection.id"
            class="show-block"
        >
            <div>
                <strong>{{ collection.name }}</strong>
                <div>Цена: {{ collection.price }}</div>

                <div v-if="collection.films">
                    Фильмы:
                    <span v-if="Array.isArray(collection.films)">
                        {{ collection.films
                            .map(film => typeof film === 'object' ? film.name : films.find(f => f.id === film)?.name ?? film)
                            .join(', ') }}
                    </span>
                </div>
            </div>

            <button
                class="btn btn-danger"
                @click="onRemoveCollection(collection)"
            >
                <i class="bi bi-x"></i>
            </button>
        </div>

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