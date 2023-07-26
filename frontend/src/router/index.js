import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminPanel from '../views/AdminPanel.vue'
import EquipmentAdmin from '../views/EquipmentAdmin.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/admin/',
    name: 'AdminPanel',
    component: AdminPanel,
  },
  {
    path: '/admin/locations/',
    name: 'LocationAdmin',
    component: () => import(/* webpackChunkName: "about" */ '../views/LocationAdmin.vue'),

  },
  {
    path: '/admin/equipment/',
    name: 'EquipmentAdmin',
    component: EquipmentAdmin,

  }


  // {
  //   path: '/admin/location/create',
  //   name: 'CreateLocation',
  //   component: () => import(/* webpackChunkName: "about" */ '../views/CreateLocation.vue')

  // }

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
