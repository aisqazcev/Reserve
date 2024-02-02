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

                <div class="form-group">
                  <label for="spaceItemType">Edificio</label>
                    <select v-model="form.building" class="form-control" id="buildintType">
                      <option v-for="building in buildingList" :key="building.id" :value="building.id">{{ building.name }}</option>
                    </select>
                </div>
                <span class="text-danger">{{ errors.space_item_type }}</span>

                <div class="form-group" v-if="form.building">
                  <label for="spaceType">Espacio</label>
                  <select v-model="form.space" class="form-control" id="spaceType" @change="fetchSpaces">
                    <option v-for="space in spaceList" :key="space.id" :value="space.id">{{ space.name }}</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="spaceItemType">Tipo de Espacio</label>
                  <select v-model="form.space_item_type" class="form-control" id="spaceItemType">
                    <option value="room">Sala</option>
                    <option value="desk">Escritorio</option>
                  </select>
                </div>
                <span class="text-danger">{{ errors.space_item_type }}</span>

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
      },
      buildingList: [],
      spaceList: [], 
      loading: false,
      errors: {
        date: "",
        start_time: "",
        end_time: "",
        booking: "",
      },
    };
  },
  mounted() {
    this.fetchBuildingList();
  },
  watch: {
  'form.building': {
    immediate: true,
    handler: 'fetchSpaces',
  },
},
  methods: {
    async fetchBuildingList() {
      try {
        const response = await axios.get(`${backendUrl}buildings/`)
        this.buildingList = response.data;
        this.fetchSpaces();
      } catch (error) {
        console.error('Error fetching building list:', error);
      }
    },
    async fetchSpaces() {
      if (this.form.building) {
        try {
          const response = await axios.get(`${backendUrl}building/${this.form.building}/spaces/`);
          this.spaceList = response.data;
        } catch (error) {
          console.error('Error fetching space list:', error);
        }
      }
    },
    async booking() {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.post(`${backendUrl}booking/`, this.form, {
                headers: { Authorization: `Token ${token}` }
            });
            this.$router.push("/bookings");
        } catch (error) {
            console.error('Error al realizar la reserva:', error.response || error);
        }
    },
  },
};
</script>