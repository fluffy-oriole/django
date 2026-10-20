import { createRouter, createWebHistory } from 'vue-router'
import FilmView from '../views/FilmView.vue'
import GenreView from '@/views/GenreView.vue'
import ActorView from '@/views/ActorView.vue'
import DirectorView from '@/views/DirectorView.vue'
import CollectionView from '@/views/CollectionView.vue'
import ReviewView from '@/views/ReviewView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/films',
      name: 'FilmView',
      component: FilmView
    },
    {
      path: '/genres',
      name: 'GenreView',
      component: GenreView
    },
    {
      path: '/reviews',
      name: 'ReviewView',
      component: ReviewView
    },
    {
      path: '/actors',
      name: 'ActorView',
      component: ActorView
    },
    {
      path: '/directors',
      name: 'DirectorView',
      component: DirectorView
    },
    {
      path: '/collections',
      name: 'CollectionView',
      component: CollectionView
    },
  ],
})

export default router
