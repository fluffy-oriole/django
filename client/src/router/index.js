import { createRouter, createWebHistory } from 'vue-router'
import FilmView from '../views/FilmView.vue'
import GenreView from '@/views/GenreView.vue'
import ActorView from '@/views/ActorView.vue'
import DirectorView from '@/views/DirectorView.vue'
import CollectionView from '@/views/CollectionView.vue'
import ReviewView from '@/views/ReviewView.vue'
import MainPage from '@/views/MainPage.vue'
import LoginPage from '@/views/LoginPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainPage
    },
    {
      path: '/login',
      component: LoginPage
    },
    {
      path: '/films',
      component: FilmView
    },
    {
      path: '/genres',
      component: GenreView
    },
    {
      path: '/reviews',
      component: ReviewView
    },
    {
      path: '/actors',
      name: 'ActorView',
      component: ActorView
    },
    {
      path: '/directors',
      component: DirectorView
    },
    {
      path: '/collections',
      component: CollectionView
    },
  ],
})

export default router
