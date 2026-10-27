<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from "axios";
import NavBar from './components/NavBar.vue';

</script>

<template>
    <nav-bar></nav-bar>
    <router-view></router-view>
</template>

<style scoped>

</style>
