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
        </div>
        <div class="container shape-container d-flex">
          <div class="col px-0">
            <div class="row">
              <div class="col-lg-6">
                <p class="lead">
                  Se ha enviado un código de verificación al correo electrónico
                  registrado, por favor, ingresa el código:
                </p>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-6 mt-4">
                <form role="form" @keydown.enter.prevent="handleEnterKey">
                  <div class="ct-example-row">
                    <div class="row">
                      <div class="col-sm">
                        <label for="date" style="color: black;">Código de verificación</label>
                        <base-input
                          alternative
                          v-model="form.verificationCode"
                          id="verificationCode"
                        ></base-input>
                      </div>
                      <div class="col-sm d-flex flex-column align-items-center justify-content-center">
                        <base-button
                          ref="verifyButton"
                          :disabled="loading"
                          type="primary"
                          class="my-4"
                          @click="verify"
                        >
                          {{ loading ? "Verificando..." : "Verificar" }}
                        </base-button>
                        <div v-if="errorMessage" class="alert alert-default error-message mt-3" role="alert">
                          <i class="fas fa-exclamation-triangle"></i>
                          {{ errorMessage }}
                        </div>
                      </div>
                    </div>
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
      email: "",
      form: {
        verificationCode: "",
      },
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
    handleEnterKey() {
      const button = this.$refs.verifyButton;
      if (button && !button.disabled) {
        button.$el.click();
      }
    },
    async verify() {
      if (this.loading) return; 

      this.loading = true; 
      this.errorMessage = '';
      this.successMessage = '';

      try {
        const response = await axios.post(
          `${backendUrl}verify_code/`,
          this.form
        );

        if (response.status === 200 && response.data.valid) {
          this.successMessage =
            "Código de verificación válido. Registrando usuario...";
          await this.register();
        } else {
          this.errorMessage =
            "Código de verificación inválido. Por favor, verifica e intenta de nuevo.";
        }
      } catch (error) {
        this.errorMessage = "Ha ocurrido un error al verificar el código.";
        console.error("Verification error:", error);
      } finally {
        this.loading = false; 
      }
    },
    async register() {
      this.loading = true;

      try {
        const response = await axios.post(`${backendUrl}register/`, this.form);
        if (response.data.detail === "Usuario registrado exitosamente") {
          this.successMessage = "Usuario creado correctamente.";
          setTimeout(() => {
            this.$router.push("/");
          }, 2000);
        } else {
          this.errorMessage =
            "Ha ocurrido un error. Por favor, inténtelo de nuevo.";
        }
      } catch (error) {
        this.errorMessage =
          "Ha ocurrido un error. Por favor, inténtelo de nuevo.";
        console.error("Register error:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
