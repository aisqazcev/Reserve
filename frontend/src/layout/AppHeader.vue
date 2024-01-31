<template>
    <header class="header-global">
        <base-nav class="navbar-main" transparent type="" effect="light" expand>
            <router-link to="/landing" class="nav-link">
                <i class="fa fa-home fa-2x" style="color: white;"></i>
            </router-link>

            <div class="separator"></div>

            <ul class="navbar-nav navbar-nav-hover align-items-lg-center">
                <base-dropdown class="nav-item" menu-classes="dropdown-menu-xl">
                    <a slot="title" href="#" class="nav-link" data-toggle="dropdown" role="button">
                        <span class="nav-link-inner--text">Facultades</span>
                    </a>
                    <div class="dropdown-menu-inner">
                        <router-link v-for="building in buildings" :key="building.id" :to="`/building/${building.id}`" class="dropdown-item">{{ building.name_complete }}</router-link>
                    </div>
                </base-dropdown>

                <!-- Botón Reservar -->
                <router-link to="/booking" class="nav-link">
                    <span class="nav-link-inner--text">Reservar</span>
                </router-link>

                <!-- Botón Mis reservas -->
                <router-link to="/bookings" class="nav-link">
                    <span class="nav-link-inner--text">Mis reservas</span>
                </router-link>
            </ul>
            <ul class="navbar-nav align-items-lg-center ml-lg-auto">
                <li class="nav-item">
                    <a class="nav-link nav-link-icon" href="https://www.facebook.com/creativetim" target="_blank" rel="noopener"
                       data-toggle="tooltip" title="Like us on Facebook">
                        <i class="fa fa-facebook-square"></i>
                        <span class="nav-link-inner--text d-lg-none">Facebook</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link nav-link-icon" href="https://www.instagram.com/creativetimofficial"
                       target="_blank" rel="noopener" data-toggle="tooltip" title="Follow us on Instagram">
                        <i class="fa fa-instagram"></i>
                        <span class="nav-link-inner--text d-lg-none">Instagram</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link nav-link-icon" href="https://twitter.com/creativetim" target="_blank" rel="noopener"
                       data-toggle="tooltip" title="Follow us on Twitter">
                        <i class="fa fa-twitter-square"></i>
                        <span class="nav-link-inner--text d-lg-none">Twitter</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link nav-link-icon" href="https://github.com/creativetimofficial/vue-argon-design-system"
                       target="_blank" rel="noopener" data-toggle="tooltip" title="Star us on Github">
                        <i class="fa fa-github"></i>
                        <span class="nav-link-inner--text d-lg-none">Github</span>
                    </a>
                </li>
                <li class="nav-item d-none d-lg-block ml-lg-4">
                    <a href="http://localhost:8080/profile" rel="noopener" class="btn btn-neutral btn-icon">
                        <span class="btn-inner--icon">
                        </span>
                        <span class="nav-link-inner--text">Perfil</span>
                    </a>
                </li>
            </ul>
            <button class="btn btn-danger" @click="logout">
                Logout
            </button>
        </base-nav>
    </header>
</template>


<script>
import BaseNav from "@/components/BaseNav";
import BaseDropdown from "@/components/BaseDropdown";
import CloseButton from "@/components/CloseButton";
import axios from 'axios';
import { backendUrl } from "../main.js";


export default {
  components: {
    BaseNav,
    CloseButton,
    BaseDropdown
  },
   data() {
        return {
            buildings: []
        };

    },

    mounted() {

        this.fetchBuildings();
    },
  methods: {
    async fetchBuildings() {
        try {

            const response = await axios.get(`${backendUrl}buildings/`);
            this.buildings = response.data;
            console.log("Lista de edificios:", this.buildings);
        } catch (error) {
            console.error("Error al cargar la lista de edificios", error);
        }
    },

    async logout() {
    console.log("LOGOUT");

    const token = localStorage.getItem('token');
      if (token) {
        axios.post(`${backendUrl}logout/`, null, {
          headers: { Authorization: `Token ${token}` }
        })
          .then(response => {
            localStorage.removeItem('token');
            this.$router.push("/");
          })
          .catch(error => {
            console.error('Error en el cierre de sesión:', error);
          });
      }
    }
  }};
</script>

<style>
    .separator {
        margin: 0 50px; 
    }
</style>