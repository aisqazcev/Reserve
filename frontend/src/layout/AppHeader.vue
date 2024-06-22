<template>
  <header class="header-global">
    <base-nav class="navbar-main" transparent type="" effect="light" expand>
      <router-link slot="brand" class="navbar-brand mr-lg-5" to="/landing">
        <img src="img/brand/logo.png" alt="logo" />
      </router-link>
      <div class="row" slot="content-header" slot-scope="{ closeMenu }">
        <div class="col-6 collapse-brand"></div>
        <div class="col-6 collapse-close">
          <close-button id="custom-close-button" @click="closeMenu"></close-button>
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

        <router-link to="/incidences" class="nav-link">
          <span class="nav-link-inner--text">Incidencias</span>
        </router-link>
      </ul>
      <ul class="navbar-nav align-items-lg-center ml-lg-auto">
        <router-link to="/profile" class="nav-link" v-show="!isDesktop">
          <span class="nav-link-inner--text">Perfil</span>
        </router-link>
        <router-link to="/" class="nav-link" v-show="!isDesktop">
          <span
            class="nav-link-inner--text"
            @click.prevent="showLogoutConfirmationCard = true"
            >Cerrar sesión</span
          >
        </router-link>

        <button
          class="btn btn-neutral d-none d-lg-inline-block"
          @click="perfil"
        >
          Perfil
        </button>
        <button
          class="btn btn-danger d-none d-lg-inline-block"
          @click="showLogoutConfirmationCard = true"
        >
          Logout
        </button>
      </ul>
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
import CloseButton from "@/components/CloseButton";
import Card from "@/components/Card";
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  components: {
    BaseNav,
    CloseButton,
    Card,
  },
  data() {
    return {
      buildings: [],
      showLogoutConfirmationCard: false,
      isDesktop: window.innerWidth >= 992,
    };
  },
  created() {
    window.addEventListener("resize", this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    handleResize() {
      this.isDesktop = window.innerWidth >= 992;
    },
    perfil() {
      this.$router.push("/profile");
    },
    confirmLogout() {
      this.showLogoutConfirmationCard = false;
      this.directLogout();
    },
    directLogout() {
      const token = localStorage.getItem("token");
      if (token) {
        axios
          .post(`${backendUrl}logout/`, null, {
            headers: { Authorization: `Token ${token}` },
          })
          .then(() => {
            localStorage.removeItem("token");
            this.$router.push("/");
          })
          .catch((error) => {
            console.error("Error en el cierre de sesión:", error);
          });
      }
    },
    cancelLogout() {
      this.showLogoutConfirmationCard = false;
    },
  },
};
</script>

<style>
#custom-close-button {
  background-color: #f8f9fa; 
}

.header-global .navbar-brand {
  font-family: "Raleway", sans-serif;
}
.header-global .navbar-nav .nav-link {
  font-family: "Raleway", sans-serif;
}


@media (max-width: 991px) {
  .d-lg-none {
    display: block;
  }
  .d-none.d-lg-inline-block {
    display: none;
  }
  .logout-confirmation {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
  }
}

@media (min-width: 992px) {
  .logout-confirmation {
    position: absolute;
    top: calc(100% + 10px);
    left: 50%;
    transform: translateX(-50%);
    width: auto;
    min-width: 300px;
  }
}
</style>
