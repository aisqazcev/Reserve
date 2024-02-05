<template>
  <header class="header-global">
    <base-nav class="navbar-main" transparent type="" effect="light" expand>
      <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
        <img src="img/brand/white.png" alt="logo" />
      </router-link>

      <div class="row" slot="content-header" slot-scope="{ closeMenu }">
        <div class="col-6 collapse-brand">
          <a
            href="https://demos.creative-tim.com/vue-argon-design-system/documentation/"
          >
            <img src="img/brand/blue.png" />
          </a>
        </div>
        <div class="col-6 collapse-close">
          <close-button @click="closeMenu"></close-button>
        </div>
      </div>

      <ul class="navbar-nav navbar-nav-hover align-items-lg-center">
        <router-link :to="{ name: 'Buildings' }" class="nav-link">
          <span class="nav-link-inner--text">Facultades</span>
        </router-link>

        <router-link to="/booking" class="nav-link">
          <span class="nav-link-inner--text">Reservar</span>
        </router-link>

        <router-link to="/mis-reservas" class="nav-link">
          <span class="nav-link-inner--text">Mis reservas</span>
        </router-link>
      </ul>
      <ul class="navbar-nav align-items-lg-center ml-lg-auto">
        <li class="nav-item d-none d-lg-block ml-lg-4">
          <a
            href="http://localhost:8080/profile"
            rel="noopener"
            class="btn btn-neutral btn-icon"
          >
            <span class="btn-inner--icon"> </span>
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
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  components: {
    BaseNav,
    CloseButton,
    BaseDropdown,
  },
  data() {
    return {
      buildings: [],
    };
  },

  mounted() {},
  methods: {
    async logout() {
      const token = localStorage.getItem("token");
      if (token) {
        axios
          .post(`${backendUrl}logout/`, null, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            localStorage.removeItem("token");
            this.$router.push("/");
          })
          .catch((error) => {
            console.error("Error en el cierre de sesión:", error);
          });
      }
    },
  },
};
</script>
