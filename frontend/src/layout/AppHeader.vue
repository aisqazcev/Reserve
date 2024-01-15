<template>
    <header class="header-global">
        <base-nav class="navbar-main" transparent type="" effect="light" expand>
            <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
                <img src="img/brand/white.png" alt="logo">
            </router-link>

            <div class="row" slot="content-header" slot-scope="{closeMenu}">
                <div class="col-6 collapse-brand">
                    <a href="https://demos.creative-tim.com/vue-argon-design-system/documentation/">
                        <img src="img/brand/blue.png">
                    </a>
                </div>
                <div class="col-6 collapse-close">
                    <close-button @click="closeMenu"></close-button>
                </div>
            </div>

            <ul class="navbar-nav navbar-nav-hover align-items-lg-center">
                <base-dropdown class="nav-item" menu-classes="dropdown-menu-xl">
                    <a slot="title" href="#" class="nav-link" data-toggle="dropdown" role="button">
                        <span class="nav-link-inner--text">Facultades</span>
                    </a>
                    <!-- Contenido del desplegable con lista de edificios -->
                    <div class="dropdown-menu-inner">
        <!-- Itera sobre los edificios disponibles -->
        <router-link v-for="building in buildings" :key="building.id" :to="`/${building.name}`" class="dropdown-item">{{ building.name_complete }}</router-link>
    </div>
                </base-dropdown>

                <!-- Botón Reservar -->
                <router-link to="/reservar" class="nav-link">
                    <span class="nav-link-inner--text">Reservar</span>
                </router-link>

                <!-- Botón Mi cuenta -->
                <router-link to="/mi-cuenta" class="nav-link">
                    <span class="nav-link-inner--text">Mi cuenta</span>
                </router-link>

                <!-- Botón Mis reservas -->
                <router-link to="/mis-reservas" class="nav-link">
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
                    <a href="https://www.creative-tim.com/product/vue-argon-design-system" target="_blank" rel="noopener"
                       class="btn btn-neutral btn-icon">
                <span class="btn-inner--icon">
                </span>
                        <span class="nav-link-inner--text">Perfil</span>
                    </a>
                </li>
            </ul>
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
            buildings: [] // Inicializa la lista de edificios
        };
    },
    mounted() {
        // Carga la lista de edificios desde el backend al montar el componente
        this.fetchBuildings();
    },
    methods: {
    async fetchBuildings() {
        try {
            // Realiza una solicitud al backend para obtener la lista de edificios
            const response = await axios.get(`${backendUrl}buildings/`); // Ajusta la ruta según tu configuración
            this.buildings = response.data;
            console.log("Lista de edificios:", this.buildings);
        } catch (error) {
            console.error("Error al cargar la lista de edificios", error);
        }
    }
}
};
</script>

