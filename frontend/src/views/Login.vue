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
                  placeholder="Usuario"
                  addon-left-icon="ni ni-email-83"
                  v-model="form.username"
                ></base-input>
                <span class="text-danger">{{ errors.username }}</span>

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
import axios from 'axios';
import { backendUrl } from "../main.js";

export default {
  name: "Login",
  data() {
    return {
      form: {
        username: "",
        password: "",
        remember: false,
      },
      loading: false,
      errors: {
        username: "",
        password: "",
        login: "",
      },
    };
  },
  methods: {
    async handleSubmit() {
       axios.post(`${backendUrl}login/`, this.form)
        .then(response => {
          const token = response.data.token;
          localStorage.setItem('token', token);
          this.$router.push("/landing");
        })
        .catch(error => {
          console.error('Error en el inicio de sesión:', error);
        });
    },
  },
};
</script>
