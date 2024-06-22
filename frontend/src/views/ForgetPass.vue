<template>
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
    <div class="container shape-container d-flex justify-content-center">
      <div class="col-lg-6">
        <div class="row">
          <div class="col-lg-12">
            <p class="lead">
              Introduce el correo electrónico con el que estás registrado y se enviará un enlace para cambiar la contraseña.
            </p>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-12 mt-4">
            <form @submit.prevent="send">
              <div class="row">
                <div class="col-sm">
                  <label for="email" style="color: black;">Email</label>
                  <base-input
                    alternative
                    placeholder="Correo electrónico"
                    type="email"
                    v-model="form.email"
                    id="email"
                  ></base-input>
                </div>
                <div class="col-sm d-flex flex-column align-items-center justify-content-center">
                  <base-button
                    :disabled="loading"
                    type="primary"
                    class="my-4"
                    @click="send"
                  >
                    Enviar
                  </base-button>
                  <div v-if="errorMessage" class="alert alert-default error-message mt-3" role="alert">
                    <i class="fas fa-exclamation-triangle"></i>
                    {{ errorMessage }}
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
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  name: "ForgotPassword",
  data() {
    return {
      form: {
        email: "",
      },
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async send() {
      try {
        this.loading = true;
        const response = await axios.post(`${backendUrl}send_recovery/`, {
          email: this.form.email,
        });
        if (response.status === 200 && response.data.verification_code) {
          localStorage.setItem('formData', JSON.stringify(this.form));
          this.form.email = ""; 
          this.errorMessage = "";
          this.$router.push({ name: 'confirm_pass' });
        } else {
          this.errorMessage = "No se pudo enviar el correo electrónico.";
        }
      } catch (error) {
        this.errorMessage = "No se pudo enviar el correo electrónico.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
