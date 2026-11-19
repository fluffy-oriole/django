<script setup>
import { ref, computed, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const reviews = ref([]);
const films = ref([]);
const loading = ref(false);
const reviewToAdd = ref({});
const reviewToEdit = ref({})
const profiles = ref([]);

const countOfReviews = ref(0);
const avgRateOfReviews = ref(0);
const maxRateOfReviews = ref(0);
const minRateOfReviews = ref(0);

const page = ref(0);
const pageItemsCount = ref(10);

const filteredReviews = computed(() => {
    return reviews.value.slice(
        page.value * pageItemsCount.value,
        (page.value + 1) * pageItemsCount.value
     );
})

const pagesCount = computed(() => {
    return Math.trunc(reviews.value.length / pageItemsCount.value + 1);
})

async function fetchReviews() {
    loading.value = true;
    try {
        const r = await axios.get('/api/reviews/');
        reviews.value = r.data;
    } finally {
        loading.value = false;
    }
}

async function fetchFilms() {
    const r = await axios.get('/api/films/');
    films.value = r.data;
}

async function fetchUsers() {
    const r = await axios.get('/api/profile/');
    profiles.value = r.data;
}

async function fetchStats() {
    const r = await axios.get('/api/reviews/stats');
    countOfReviews.value = r.data.count;
    avgRateOfReviews.value = r.data.avg;
    maxRateOfReviews.value = r.data.max;
    minRateOfReviews.value = r.data.min;
}

async function onLoadClick() {
    await Promise.all([
        fetchReviews(),
        fetchFilms(),
        fetchUsers(),
        fetchStats()
    ]);
}

onBeforeMount(() => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
    onLoadClick();
});

async function onReviewAdd() {
    await axios.post('/api/reviews/', {
        ...reviewToAdd.value,
    });

    reviewToAdd.value = {};
    await fetchReviews();
    await fetchStats();
}

async function onRemoveReview(review) {
    await axios.delete(`/api/reviews/${review.id}/`);
    await fetchReviews();
    await fetchStats();
}

async function onReviewEditClick(review) {
    reviewToEdit.value = { ...review };
    console.log("Редактируем:", reviewToEdit.value);
}

async function onUpdateReview() {
    await axios.put(`/api/reviews/${reviewToEdit.value.id}/`, {
    ...reviewToEdit.value,
    });
    await fetchReviews();
    await fetchStats();
}

</script>

<template>
    <div class="modal fade" id="editReviewModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">
                        редактировать рецензию
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
                                <select class="form-select" v-model="reviewToEdit.film">
                                    <option :value="film.id" v-for="film in films" :key="film.id">
                                        {{ film.name }}
                                    </option>
                                </select>
                                <label>Фильм</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <textarea
                                    class="form-control"
                                    v-model="reviewToEdit.review_text"
                                ></textarea>
                                <label>Текст рецензии</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="reviewToEdit.author">
                                    <option :value="profile.id" v-for="profile in profiles" :key="profile.id">
                                        {{ profile.id }}
                                    </option>
                                </select>
                                <label>Автор</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col">
                            <div class="form-floating">
                                <input
                                    type="number"
                                    class="form-control"
                                    v-model.number="reviewToEdit.rate"
                                />
                                <label>Оценка</label>
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
                        @click="onUpdateReview"
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
            <div>Количество рецензий: {{ countOfReviews }}</div>
            <div>Средняя оценка: {{ avgRateOfReviews }}</div>
            <div>Максимальная оценка: {{ maxRateOfReviews }}</div>
            <div>Минимальная оценка: {{ minRateOfReviews }}</div>
        </div>

        <strong><div>Рецензии</div></strong>

        <div
            v-for="review in filteredReviews"
            :key="review.id"
            class="show-block"
        >
            <div>
                <strong>
                    {{ review.film }}
                </strong>
                <div>{{ review.review_text }}</div>
                <div>Автор: {{ review.author }}</div>
                <div>Оценка: {{ review.rate }}</div>
            </div>

            <button
                class="btn btn-success"
                @click="onReviewEditClick(review)"
                data-bs-toggle="modal"
                data-bs-target="#editReviewModal"
            >
                <i class="bi bi-pen-fill"></i>
            </button>

            <button
                class="btn btn-danger"
                @click="onRemoveReview(review)"
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

        <strong><div>Добавить рецензию</div></strong>

        <form @submit.prevent.stop="onReviewAdd">
            <div class="row">
                <div class="col-auto">
                    <div class="form-floating">
                        <select
                            class="form-select"
                            v-model="reviewToAdd.film"
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
                        <label>Фильм</label>
                    </div>
                </div>

                <div class="col">
                    <div class="form-floating">
                        <textarea
                            class="form-control"
                            v-model="reviewToAdd.review_text"
                            required
                        ></textarea>
                        <label>Текст рецензии</label>
                    </div>
                </div>

                <div class="col">
                    <div class="form-floating">
                        <select class="form-select" v-model="reviewToAdd.author" required>
                            <option :value="profile.id" v-for="profile in profiles" :key="profile.id">
                                {{ profile.id }}
                            </option>
                        </select>
                        <label>Автор</label>
                    </div>
                </div>

                <div class="col-auto">
                    <div class="form-floating">
                        <input
                            type="number"
                            class="form-control"
                            v-model.number="reviewToAdd.rate"
                            required
                        />
                        <label>Оценка</label>
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