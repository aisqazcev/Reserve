<template>
  <section class="section section-shaped section-lg my-0">
    <div class="shape shape-style-1 bg-gradient-default">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container pt-lg-md">
      <div class="row justify-content-center">
        <div class="col-lg-5">
          <card
            type="secondary"
            shadow
            header-classes="bg-white pb-5"
            body-classes="px-lg-5 py-lg-5"
            class="border-0"
          >
            <template>
              <div class="text-center text-muted mb-4">
                <small>Introduce tus credenciales</small>
              </div>
              <form @submit.prevent="handleSubmit" role="form">
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Usuario o Correo Electrónico"
                  addon-left-icon="ni ni-email-83"
                  v-model="form.usernameOrEmail"
                ></base-input>
                <span class="text-danger">{{ errors.usernameOrEmail }}</span>

                <base-input
                  alternative
                  type="password"
                  placeholder="Contraseña"
                  addon-left-icon="ni ni-lock-circle-open"
                  v-model="form.password"
                ></base-input>
                <span class="text-danger">{{ errors.password }}</span>

                <base-checkbox v-model="form.remember">
                  Recordarme
                </base-checkbox>
                <div class="text-center">
                  <base-button
                    :disabled="loading"
                    type="primary"
                    class="my-4"
                    @click="handleSubmit"
                  >
                    Iniciar
                  </base-button>
                </div>
              </form>
              <span class="text-danger">{{ errors.login }}</span>
            </template>
          </card>
          <div class="row mt-3">
            <div class="col-6">
              <router-link to="#" class="text-light">
                <small>¿Olivdaste tu contraseña?</small>
              </router-link>
            </div>
            <div class="col-6 text-right">
              <router-link to="/register" class="text-light">
                <small>Registrarse</small>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  name: "Login",
  data() {
    return {
      form: {
        usernameOrEmail: "",
        password: "",
        remember: false,
      },
      loading: false,
      errors: {
        usernameOrEmail: "",
        password: "",
        login: "",
      },
    };
  },
  methods: {
    async handleSubmit() {
      axios
        .post(`${backendUrl}login/`, {
          username_or_email: this.form.usernameOrEmail,
          password: this.form.password,
          remember: this.form.remember,
        })
        .then((response) => {
          const token = response.data.token;
          localStorage.setItem("token", token);
          this.$router.push("/landing");
        })
        .catch((error) => {
          console.error("Error en el inicio de sesión:", error);
          if (error.response && error.response.status === 400) {
            this.errors.login = "Credenciales inválidas";
            this.errors.usernameOrEmail =
              error.response.data.username_or_email[0];
          } else {
            this.errors.login =
              "Error en el inicio de sesión. Por favor, inténtalo de nuevo.";
          }
        });
    },
  },
};
</script>
