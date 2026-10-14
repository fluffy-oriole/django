<script setup>
import { ref, onBeforeMount } from 'vue';
import Cookies from 'js-cookie';
import axios from "axios";

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    onLoadClick();
});
</script>

<template>

</template>

<style scoped>
</style>