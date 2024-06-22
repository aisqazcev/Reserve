<template>
  <section class="section section-shaped section-lg my-0">
    <div class="shape shape-style-1 color">
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
              <div class="text-center mb-3">
                <small>Crea tu usuario</small>
              </div>
              <form @submit.prevent="register" role="form" @keydown.enter.prevent="handleEnterKey">
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Usuario"
                  v-model="form.username"
                  addon-left-icon="ni ni-hat-3"
                ></base-input>
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Nombre"
                  v-model="form.name"
                  addon-left-icon="ni ni-single-02"
                ></base-input>
                <base-input
                  alternative
                  class="mb-3"
                  placeholder="Email"
                  v-model="form.email"
                  addon-left-icon="ni ni-email-83"
                ></base-input>
                <base-input
                  alternative
                  type="password"
                  placeholder="Contraseña"
                  v-model="form.password"
                  addon-left-icon="ni ni-lock-circle-open"
                ></base-input>
                <base-input
                  alternative
                  type="password"
                  placeholder="Confirmar Contraseña"
                  v-model="form.password2"
                  addon-left-icon="ni ni-lock-circle-open"
                ></base-input>
                <i
                  class="fas fa-question-circle"
                  size="sm"
                  type="default"
                  v-b-popover.hover.left="
                    'La contraseña debe contener al menos 8 caracteres, incluyendo al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.'
                  "
                  title="Información sobre la contraseña"
                >
                </i>

                <div class="text-center">
                  <base-button
                    ref="submitButton"
                    :disabled="!isValidForm || loading"
                    type="primary"
                    class="my-4"
                    @click="send_confirmation"
                  >
                    {{ loading ? "Creando..." : "Crear Usuario" }}
                  </base-button>
                </div>
                <div class="text-center mt-3">
                  <router-link to="/">
                    Volver al inicio de sesión
                  </router-link>
                </div>
                <base-alert
                  v-if="successMessage"
                  type="success"
                  dismissible
                  class="text-center mt-3"
                >
                  <span class="alert-inner--icon"><i class="ni ni-like-2"></i></span>
                  <span class="alert-inner--text"><strong>¡Todo listo!</strong> {{ successMessage }}</span>
                </base-alert>
                <div v-if="errorMessage" class="text-danger text-center mt-3">
                  {{ errorMessage }}
                </div>
              </form>
            </template>
          </card>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";
import { VBTooltip } from "bootstrap-vue/esm/directives/tooltip/tooltip";
import { VBPopover } from "bootstrap-vue/esm/directives/popover/popover";
import router from '../router.js';

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default {
  name: "SignUp",
  data() {
    return {
      form: {
        username: "",
        password: "",
        password2: "",
        name: "",
        email: "",
      },
      errors: [],
      loading: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  directives: {
    BTooltip: VBTooltip,
    BPopover: VBPopover,
  },
  computed: {
    isValidForm() {
      return (
        this.form.username.trim() !== "" &&
        this.form.name.trim() !== "" &&
        this.form.email.trim() !== "" &&
        this.form.password.trim() !== "" &&
        this.form.password2.trim() !== "" &&
        this.isSecurePassword() &&
        this.form.password === this.form.password2
      );
    },
  },
  methods: {
    handleEnterKey() {
      const button = this.$refs.submitButton;
      if (button && !button.disabled) { 
        button.$el.click();
      }
    },
    async send_confirmation() {
      try {
        const response = await axios.post(`${backendUrl}send_email/`, { email: this.form.email });
        if (response.status === 200) {
          this.successMessage = "Correo de confirmación enviado con éxito.";
          localStorage.setItem('formData', JSON.stringify(this.form));
          this.$router.push({ name: 'confirm_register' });
        } else {
          console.error('Respuesta inesperada:', response);
          this.errorMessage = "Error al enviar el correo de confirmación.";
        }
      } catch (error) {
        this.errorMessage = "Ha ocurrido un error al enviar el correo de confirmación.";
        console.error("Confirmation email error:", error);
      }
    },

    isSecurePassword() {
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      return regex.test(this.form.password);
    },
  },
};
</script>
