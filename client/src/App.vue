<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from "axios";

</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav">
            <li class="nav-item active">
                <router-link class="nav-link" to="/films">Фильмы</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/genres">Жанры</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/reviews">Отзывы</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/directors">Режиссеры</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/actors">Актеры</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/collections">Коллекции</router-link>
            </li>
            </ul>
            
            <ul class="navbar-nav">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Пользователь
                    </a>
                    <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="/admin">Админка</a></li>
                    </ul>
                </li>
            </ul>
        </div>
        </nav>
    <router-view></router-view>
</template>

<style scoped>

</style>
