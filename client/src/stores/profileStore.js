import { defineStore } from "pinia";
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

const useProfileStore = defineStore('profileStore', () => {
    const is_authenticated = ref(false);
    const user_name = ref(null);

    async function fetchMe() {
        const r = await axios.get("api/profile/me/");
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        is_authenticated.value = r.data.is_authenticated;
        user_name.value = r.data.is_authenticated ? r.data.user_name : null;
    }

    async function  login(username, password ) {
        const r = await axios.post('/api/profile/login/', {
            username: username,
            password: password
        })
        fetchMe();
    }

    async function  logout() {
        const r = await axios.post('/api/profile/logout/');
        fetchMe();
    }

    onBeforeMount( () => {
        fetchMe();
    })

    return {
        is_authenticated,
        user_name,
        fetchMe,
        login,
        logout,
        
    }
})

export default useProfileStore;