<template>
  <div>
    <div class="position">
      <section class="section section-shaped section-lg my-0">
        <div class="shape shape-style-2 shape-default">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="container shape-container d-flex">
          <div class="col px-0">
            <div class="row">
              <div class="col-lg-6">
                <p class="lead" v-if="!codeVerified">
                  Se ha enviado un código de verificación al correo electrónico
                  registrado, por favor, ingresa el código:
                </p>
                <p class="lead" v-else>
                  Ingresa tu nueva contraseña:
                </p>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-6 mt-4">
                <form @submit.prevent="codeVerified ? change_pass() : verify()">
                  <div v-if="!codeVerified" class="ct-example-row">
                    <div class="row">
                      <div class="col-sm">
                        <label for="verificationCode" style="color: black;">
                          Código de verificación
                        </label>
                        <base-input
                          alternative
                          type=""
                          v-model="form.verificationCode"
                          id="verificationCode"
                          @keydown.enter.prevent="verify()"
                        ></base-input>
                      </div>
                      <div
                        class="col-sm d-flex flex-column align-items-center justify-content-center"
                      >
                        <base-button
                          :disabled="loading"
                          type="primary"
                          class="my-4"
                          @click="verify()"
                        >
                          Verificar
                        </base-button>
                        <div
                          v-if="errorMessage"
                          class="alert alert-default error-message mt-3"
                          role="alert"
                        >
                          <i class="fas fa-exclamation-triangle"></i>
                          {{ errorMessage }}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="ct-example-row">
                    <div class="row">
                      <div class="col-sm">
                        <label for="newPassword" style="color: black;">
                          Nueva contraseña
                        </label>
                        <base-input
                          alternative
                          type="password"
                          v-model="form.newPassword"
                          id="newPassword"
                          @keydown.enter.prevent="change_pass()"
                        ></base-input>
                      </div>
                    </div>
                    <div class="row">
                      <div class="col-sm">
                        <label for="confirmPassword" style="color: black;">
                          Confirmar contraseña
                        </label>
                        <base-input
                          alternative
                          type="password"
                          v-model="form.confirmPassword"
                          id="confirmPassword"
                          @keydown.enter.prevent="change_pass()"
                        ></base-input>
                      </div>
                    </div>
                    <div class="row">
                      <div
                        class="col-sm d-flex flex-column align-items-center justify-content-center"
                      >
                        <base-button
                          :disabled="loading"
                          type="primary"
                          class="my-4"
                          @click="change_pass()"
                        >
                          Cambiar contraseña
                        </base-button>
                        <div
                          v-if="errorMessage"
                          class="alert alert-default error-message mt-3"
                          role="alert"
                        >
                          <i class="fas fa-exclamation-triangle"></i>
                          {{ errorMessage }}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="text-center mt-3">
                    <router-link to="/">Volver al inicio de sesión</router-link>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  data() {
    return {
      form: {
        verificationCode: "",
        email: "",
        newPassword: "",
        confirmPassword: "",
      },
      codeVerified: false,
      loading: false,
      errorMessage: "",
    };
  },
  created() {
    const formData = localStorage.getItem("formData");
    if (formData) {
      this.form = JSON.parse(formData);
      if (this.form.verificationCode) {
        this.verificationCode = this.form.verificationCode;
      }
    }
  },
  methods: {
    async verify() {
      try {
        const response = await axios.post(
          `${backendUrl}verify_code/`,
          this.form
        );

        if (response.status === 200 && response.data.valid) {
          this.successMessage =
            "Código de verificación válido. Registrando usuario...";
          this.codeVerified = true;
        } else {
          this.errorMessage =
            "Código de verificación inválido. Por favor, verifica e intenta de nuevo.";
        }
      } catch (error) {
        this.errorMessage = "Ha ocurrido un error al verificar el código.";
        console.error("Verification error:", error);
      }
    },
    async change_pass() {
      try {
        this.loading = true;
        const response = await axios.post(`${backendUrl}change_pass/`, {
          email: this.form.email,
          new_password: this.form.newPassword,
          confirm_new_password: this.form.confirmPassword,
        });

        if (response.status === 200) {
          this.successMessage = "Contraseña cambiada exitosamente.";
          localStorage.removeItem("formData");
          this.$router.push("/");
        } else {
          this.errorMessage =
            "Ha ocurrido un error al cambiar la contraseña. Por favor, inténtalo de nuevo.";
        }
      } catch (error) {
        this.errorMessage =
          "Ha ocurrido un error al cambiar la contraseña. Por favor, inténtalo de nuevo.";
        console.error("Change password error:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Estilos específicos para este componente */
</style>
