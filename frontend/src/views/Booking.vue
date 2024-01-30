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
                <small>Reserva tu espacio</small>
              </div>
              <form @submit.prevent="booking" role="form">
                <base-input
                  alternative
                  type="date"
                  placeholder="Fecha"
                  v-model="form.date"
                ></base-input>
                <span class="text-danger">{{ errors.date }}</span>

                <base-input
                  alternative
                  type="time"
                  placeholder="Hora de inicio"
                  v-model="form.start_time"
                ></base-input>
                <span class="text-danger">{{ errors.start_time }}</span>

                <base-input
                  alternative
                  type="time"
                  placeholder="Hora de fin"
                  v-model="form.end_time"
                ></base-input>
                <span class="text-danger">{{ errors.end_time }}</span>

                <base-input
                  alternative
                  type="email"
                  placeholder="Email"
                  v-model="form.email"
                ></base-input>
                <span class="text-danger">{{ errors.email }}</span>

                <div class="text-center">
                  <base-button
                    :disabled="loading"
                    type="primary"
                    class="my-4"
                    @click="booking"
                  >
                    Reservar
                  </base-button>
                </div>
              </form>
              <span class="text-danger">{{ errors.booking }}</span>
            </template>
          </card>
          <!-- Otras secciones de la página, si es necesario -->
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import { backendUrl } from "../main.js";

export default {
  name: "booking",
  data() {
    return {
      form: {
        date: "",
        start_time: "",
        end_time: "",
        email: "",
      },
      loading: false,
      errors: {
        date: "",
        start_time: "",
        end_time: "",
        email: "",
        booking: "",
      },
    };
  },
  methods: {
    async booking() {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.post(`${backendUrl}booking/`, this.form, {
                headers: { Authorization: `Token ${token}` }
            });
            this.$router.push("/landing");
        } catch (error) {
            console.error('Error al realizar la reserva:', error.response || error);
        }
    },
  },
};
</script>