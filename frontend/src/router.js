import Vue from "vue";
import Router from "vue-router";
import AppHeader from "./layout/AppHeader";
import AppFooter from "./layout/AppFooter";
import Landing from "./views/Landing.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Profile from "./views/Profile.vue";
import SpacesByBuilding from './views/SpacesByBuilding.vue';
import Booking from "./views/Booking.vue";
import Bookings from "./views/MyBookings.vue";

Vue.use(Router);

const router = new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "login",
      components: {
        default: Login,
        footer: AppFooter
      }
    },
    {
      path: "/landing",
      name: "landing",
      components: {
        header: AppHeader,
        default: Landing,
        footer: AppFooter
      },
      meta: { requiresAuth: true }
    },
    {
      path: "/register",
      name: "register",
      components: {
        default: Register,
        footer: AppFooter
      }
    },
    {
      path: "/profile",
      name: "profile",
      components: {
        header: AppHeader,
        default: Profile,
        footer: AppFooter
      },
      meta: { requiresAuth: true }
    },
    {
      path: "/building/:buildingId",
      name: "building-spaces",
      components: {
        header: AppHeader,
        default: SpacesByBuilding,
        footer: AppFooter
      }
    },
    {
      path: "/booking",
      name: "booking",
      components: {
        header: AppHeader,
        default: Booking,
        footer: AppFooter,
      },
    },
    {
      path: "/bookings",
      name: "bookings",
      components: {
        header: AppHeader,
        default: Bookings,
        footer: AppFooter,
      },
    },
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (!localStorage.getItem('token')) {
      next({ name: 'login' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;