<template>
  <header class="header-global">
    <base-nav class="navbar-main" transparent type="" effect="light" expand>
    <router-link to="/landing" class="nav-link">
    <i class="fa fa-home fa-2x" style="color: #be0f2e;"></i>
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

        <router-link to="/bookings" class="nav-link">
          <span class="nav-link-inner--text">Mis reservas</span>
        </router-link>
      </ul>
      <ul class="navbar-nav align-items-lg-center ml-lg-auto">
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="https://www.facebook.com/creativetim"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Like us on Facebook"
          >
            <i class="fa fa-facebook-square"></i>
            <span class="nav-link-inner--text d-lg-none">Facebook</span>
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="https://www.instagram.com/creativetimofficial"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Follow us on Instagram"
          >
            <i class="fa fa-instagram"></i>
            <span class="nav-link-inner--text d-lg-none">Instagram</span>
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="https://twitter.com/creativetim"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Follow us on Twitter"
          >
            <i class="fa fa-twitter-square"></i>
            <span class="nav-link-inner--text d-lg-none">Twitter</span>
          </a>
        </li>
        <li class="nav-item">
          <a
            class="nav-link nav-link-icon"
            href="https://github.com/creativetimofficial/vue-argon-design-system"
            target="_blank"
            rel="noopener"
            data-toggle="tooltip"
            title="Star us on Github"
          >
            <i class="fa fa-github"></i>
            <span class="nav-link-inner--text d-lg-none">Github</span>
          </a>
        </li>
      </ul>
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
  font-family: 'Raleway', sans-serif;
}

.header-global .navbar-nav .nav-link {
  font-family: 'Raleway', sans-serif;
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
</style>
