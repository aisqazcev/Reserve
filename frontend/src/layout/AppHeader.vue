<template>
  <header class="header-global">
    <base-nav class="navbar-main" transparent type="" effect="light" expand>
      <router-link slot="brand" class="navbar-brand mr-lg-5" to="/landing">
        <img src="img/brand/logo.png" alt="logo"
      /></router-link>
      <div class="row" slot="content-header" slot-scope="{ closeMenu }">
        <div class="col-6 collapse-brand">
          <router-link to="/landing" class="nav-link">
            <img src="img/brand/seateasyNameLogo.png" />
          </router-link>
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

        <router-link to="/bookings" class="nav-link">
          <span class="nav-link-inner--text">Mis reservas</span>
        </router-link>
      </ul>
      <ul class="navbar-nav align-items-lg-center ml-lg-auto"></ul>
      <button class="btn btn-neutral" @click="perfil">
        Perfil
      </button>
      <button class="btn btn-danger" @click="showLogoutConfirmationCard = true">
        Logout
      </button>
      <div v-if="showLogoutConfirmationCard" class="logout-confirmation">
        <card shadow class="bg-white">
          <div class="text-center mb-4 text-primary">
            <h6>¿Estás seguro de que quieres cerrar sesión?</h6>
          </div>
          <div class="text-center">
            <base-button type="success" class="mr-2" @click="confirmLogout">
              Aceptar
            </base-button>
            <base-button type="danger" @click="cancelLogout">
              Cancelar
            </base-button>
          </div>
        </card>
      </div>
    </base-nav>
  </header>
</template>

<script>
import BaseNav from "@/components/BaseNav";
import BaseDropdown from "@/components/BaseDropdown";
import CloseButton from "@/components/CloseButton";
import Card from "@/components/Card";
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  components: {
    BaseNav,
    CloseButton,
    BaseDropdown,
    Card,
  },
  data() {
    return {
      buildings: [],
      showLogoutConfirmationCard: false,
    };
  },

  mounted() {},
  methods: {
    perfil() {
      this.$router.push("/profile");
    },
    showLogoutConfirmationDialog() {
      this.showConfirmationDialog = true;
    },
    cancelLogout() {
      this.showLogoutConfirmationCard = false;
    },
    confirmLogout() {
      this.showLogoutConfirmationCard = false;
      this.logout();
    },
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

<style>
.header-global .navbar-brand {
  font-family: "Raleway", sans-serif;
}

.header-global .navbar-nav .nav-link {
  font-family: "Raleway", sans-serif;
}
.separator {
  margin: 0 50px;
}
.logout-confirmation {
  position: absolute;
  top: calc(100% + 10px); /* Ajusta el valor según sea necesario */
  left: 50%;
  transform: translateX(-50%);
}
.logo {
  margin-right: 10px; /* Ajusta el margen según sea necesario */
}
</style>
