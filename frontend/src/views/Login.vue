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
              <form
                @submit.prevent="handleSubmit"
                @keydown.enter="handleEnterKey"
                role="form"
              >
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Usuario o Correo Electrónico"
                  addon-left-icon="ni ni-email-83"
                  v-model="form.usernameOrEmail"
                ></base-input>

                <base-input
                  alternative
                  type="password"
                  placeholder="Contraseña"
                  addon-left-icon="ni ni-lock-circle-open"
                  v-model="form.password"
                ></base-input>

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
                <div class="col-md-12">
                  <dt>
                    <div
                      v-if="errorMessage"
                      class="alert alert-default error-message"
                      role="alert"
                    >
                      <i class="fas fa-exclamation-triangle"></i>
                      {{ errorMessage }}
                    </div>
                  </dt>
                </div>
              </form>
            </template>
          </card>
          <div class="row mt-3">
            <div class="col-6">
              <router-link to="/forget_pass" class="text-light">
                <small>¿Olvidaste tu contraseña?</small>
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
      errorMessage: "",
    };
  },
  mounted() {
    this.checkRememberedUser();
  },
  watch: {
    'form.remember': function(newVal) {
      if (!newVal) {
        this.clearRememberedUser();
      }
    },
    'form.usernameOrEmail': function(newVal) {
      if(!newVal){
        this.form.password = "";
      }
    }
  },
  methods: {
    checkRememberedUser() {
      const rememberedUser = localStorage.getItem("rememberedUser");
      const rememberedPassword = localStorage.getItem("rememberedPassword");
      if (rememberedUser && rememberedPassword) {
        this.form.usernameOrEmail = JSON.parse(rememberedUser);
        this.form.password = JSON.parse(rememberedPassword);
        this.form.remember = true;
      }
    },
    clearRememberedUser() {
      localStorage.removeItem("rememberedUser");
      localStorage.removeItem("rememberedPassword");
      this.form.usernameOrEmail = "";
      this.form.password = "";
    },
    async handleSubmit() {
      if (!this.form.usernameOrEmail || !this.form.password) {
        this.errorMessage = "Los campos no pueden estar vacíos";
        return;
      }
      if (this.form.remember) {
        localStorage.setItem(
          "rememberedUser",
          JSON.stringify(this.form.usernameOrEmail)
        );
        localStorage.setItem("rememberedPassword", JSON.stringify(this.form.password));
      } else {
        localStorage.removeItem("rememberedUser");
        localStorage.removeItem("rememberedPassword");
      }
      try {
        const response = await axios.post(`${backendUrl}login/`, {
          username_or_email: this.form.usernameOrEmail,
          password: this.form.password,
          remember: this.form.remember,
        });

        const token = response.data.token;
        localStorage.setItem("token", token);
        this.$router.push("/landing");
      } catch (error) {
        console.error("Error en el inicio de sesión:", error);
        if (error.response && error.response.status === 400) {
          this.errorMessage = "Credenciales incorrectas";
        } else {
          this.errorMessage =
            "Error en el inicio de sesión. Por favor, inténtalo de nuevo.";
        }
      }
    },
    handleEnterKey(event) {
      if (event.key === "Enter") {
        this.handleSubmit();
      }
    },
  },
};
</script>
