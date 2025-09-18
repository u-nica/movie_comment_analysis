import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import ProvinceView from '../views/Province.vue'
import DataEdit from '../views/DataEdit.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/province/:name',
      name: 'province',
      component: ProvinceView,
      props: true
    },
    {
      path: '/data-edit',
      name: 'data-edit',
      component: DataEdit,
      props: true
    }
  ]
})

export default router