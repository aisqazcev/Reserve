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
                  <a href="#" @click="openImageSelectionModal">
                    <img :src="imageUrlWithTimestamp(selectedImage)" class="rounded-circle" />
                  </a>
                </div>
              </div>
              <div class="col-lg-4 order-lg-3 text-lg-right align-self-lg-center"></div>
            </div>
            <div style="margin-top: 100px;"></div>

            <div class="mt-5 py-5 border-top text-center">
              <h3>{{ userData ? userData.name : "Nombre Desconocido" }}</h3>
              <div class="h6 font-weight-300">
                <i class="ni location_pin mr-2"></i>
                {{ userData ? userData.username : "Username Desconocido" }}
              </div>
              <div class="text-center">
                <base-button type="primary" @click="openChangePasswordModal">
                  Cambiar Contraseña
                </base-button>
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
                    <div v-if="errorMessage" class="text-danger mb-3">{{ errorMessage }}</div>
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
            <modal
              v-if="showImageSelectionModal"
              :show.sync="showImageSelectionModal"
              body-classes="p-0"
              modal-classes="modal-dialog-centered"
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
                    <h2>Seleccionar Imagen de Perfil</h2>
                  </div>
                  <div class="row">
                    <div class="col-4" v-for="image in profileImages" :key="image">
                      <img
                        :src="image"
                        class="img-thumbnail"
                        @click="selectImage(image)"
                      />
                    </div>
                  </div>
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
      showImageSelectionModal: false,
      currentPassword: "",
      newPassword: "",
      confirmNewPassword: "",
      errorMessage: "",
      profileImages: [
        "img/theme/pato.jpg",
        "img/theme/gato.jpg",
        "img/theme/perro.jpg",
      ],
      selectedImage: "img/theme/pato.jpg"
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
            if (this.userData.profile_image) {
              this.selectedImage = this.userData.profile_image;
            }
          })
          .catch((error) => {
            console.error("Error en la obtención de datos del perfil:", error);
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
          this.errorMessage = "";
        })
        .catch((error) => {
          if (error.response && error.response.data) {
            const errors = error.response.data;
            if (errors.new_password) {
              this.errorMessage = errors.new_password.join(", ");
            } else if (errors.detail) {
              this.errorMessage = errors.detail;
            } else {
              this.errorMessage = "Error al cambiar la contraseña.";
            }
          } else {
            this.errorMessage = "Error al cambiar la contraseña.";
          }
        });
    },
    openImageSelectionModal() {
      this.showImageSelectionModal = true;
    },
    selectImage(image) {
      this.selectedImage = image;
      this.updateProfileImage();
      this.showImageSelectionModal = false;
    },
    updateProfileImage() {
      const token = localStorage.getItem("token");
      axios
        .post(
          `${backendUrl}update-profile-image/`,
          {
            profile_image: this.selectedImage,
          },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        )
        .then((response) => {
          this.fetchUserData(); 
        })
        .catch((error) => {
          console.error("Error al actualizar la imagen de perfil:", error);
        });
    },
    imageUrlWithTimestamp(url) {
      return `${url}?timestamp=${new Date().getTime()}`;
    }
  },
};
</script>

<style>
.card-profile-image {
  position: relative;
  margin-top: -50px;
}

.card-profile-image img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 3px solid #fff;
  cursor: pointer; 
}

.img-thumbnail {
  width: 100px;
  height: 100px;
  cursor: pointer;
}
</style>
