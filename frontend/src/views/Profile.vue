<template>
  <div class="profile-page">
    <section class="section-profile-cover section-shaped my-0">
      <div class="shape shape-style-1 shape-skew alpha-4">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </section>
    <section class="section section-skew">
      <div class="container">
        <card shadow class="card-profile mt--300" no-body>
          <div class="px-4">
            <div class="row justify-content-center">
              <div class="col-lg-3 order-lg-2">
                <div class="card-profile-image">
                  <a href="#">
                    <img
                      v-lazy="'img/theme/img-profile.jpg'"
                      class="rounded-circle"
                    />
                  </a>
                </div>
              </div>
              <div
                class="col-lg-4 order-lg-3 text-lg-right align-self-lg-center"
              >
                <div class="card-profile-actions py-4 mt-lg-0">
                  <base-button type="primary" size="sm" class="mr-4"
                    >Invitaciones</base-button
                  >
                  <base-button type="default" size="sm" class="float-right"
                    >Incidencias</base-button
                  >
                </div>
              </div>
            </div>

            <div class="mt-5 py-5 border-top text-center">
              <h3>{{ userData ? userData.name : "Nombre Desconocido" }}</h3>
              <div class="h6 font-weight-300">
                <i class="ni location_pin mr-2"></i>
                {{ userData ? userData.username : "Username Desconocido" }}
              </div>
              <div class="text-center">
              <base-button type="primary" @click="openChangePasswordModal"
                >Cambiar Contraseña</base-button
              >
            </div>
            </div>

           

            <modal
              v-if="showChangePasswordModal"
              :show.sync="showChangePasswordModal"
              body-classes="p-0"
              modal-classes="modal-dialog-centered modal-sm"
            >
              <card
                type="secondary"
                shadow
                header-classes="bg-white pb-5"
                body-classes="px-lg-5 py-lg-5"
                class="border-0"
              >
                <template>
                  <div class="text-center text-muted mb-4">
                    <h2>Cambiar Contraseña</h2>
                  </div>
                  <form @submit.prevent="changePassword">
                    <base-input
                      alternative
                      class="mb-3"
                      placeholder="Contraseña Actual"
                      v-model="currentPassword"
                      type="password"
                    ></base-input>
                    <base-input
                      alternative
                      class="mb-3"
                      placeholder="Nueva Contraseña"
                      v-model="newPassword"
                      type="password"
                    ></base-input>
                    <base-input
                      alternative
                      class="mb-3"
                      placeholder="Confirmar Nueva Contraseña"
                      v-model="confirmNewPassword"
                      type="password"
                    ></base-input>
                    <div class="text-center">
                      <base-button
                        type="primary"
                        class="my-4"
                        @click="changePassword"
                        >Guardar Cambios</base-button
                      >
                    </div>
                  </form>
                </template>
              </card>
            </modal>
          </div>
        </card>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  data() {
    return {
      userData: null,
      showChangePasswordModal: false,
      currentPassword: "",
      newPassword: "",
      confirmNewPassword: "",
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    fetchUserData() {
      const token = localStorage.getItem("token");
      if (token) {
        axios
          .get(`${backendUrl}profile/`, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.userData = response.data;
          })
          .catch((error) => {
            console.error("Error en el cierre de sesión:", error);
          });
      } else {
        console.error("No se encontró el token de autenticación.");
      }
    },

    openChangePasswordModal() {
      this.showChangePasswordModal = true;
    },
    closeChangePasswordModal() {
      this.showChangePasswordModal = false;
    },
    changePassword() {
      const token = localStorage.getItem("token");
      axios
        .post(
          `${backendUrl}change-password/`,
          {
            current_password: this.currentPassword,
            new_password: this.newPassword,
            confirm_new_password: this.confirmNewPassword,
          },
          {
            headers: {
              Authorization: `Token ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((response) => {
          this.showChangePasswordModal = false;
        })
        .catch((error) => {
          console.error("Error al cambiar la contraseña:", error);
        });
    },
  },
};
</script>

<style></style>
