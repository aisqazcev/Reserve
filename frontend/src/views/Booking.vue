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
                  <label for="campusType">Campus</label>
                    <select v-model="form.campus" class="form-control" id="campusType">
                      <option v-for="campus in campusList" :key="campus.id" :value="campus.name">{{ campus.name }}</option>
                    </select>
                </div>

                <div class="form-group" v-if="form.campus">
                  <label for="buildingType">Edificio</label>
                  <select v-model="form.building" class="form-control" id="spaceType" @change="fetchBuilding">
                    <option v-for="building in buildingList" :key="building.id" :value="building.id">{{ building.name }}</option>
                  </select>
                </div>

                <!-- <div class="form-group">
                  <label for="spaceItemType">Tipo de Espacio</label>
                  <select v-model="form.space_item_type" class="form-control" id="spaceItemType">
                    <option value="room">Sala</option>
                    <option value="desk">Escritorio</option>
                  </select>
                </div>
                <span class="text-danger">{{ errors.space_item_type }}</span> -->

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
        campus: "",
        facultad: "",
      },
      campusList: [],
      buildingList: [],
      loading: false,
      errors: {
        date: "",
        start_time: "",
        end_time: "",
        campus: "",
        facultad: "",
        booking: "",
      },
    };
  },
  mounted() {
    this.fetchCampusList();
  },
  watch: {
  'form.campus': {
    immediate: true,
    handler: 'fetchBuilding',
  },
},
  methods: {
    async fetchCampusList() {
      try {
        const response = await axios.get(`${backendUrl}campuses/`)
        this.campusList = response.data;
      } catch (error) {
        console.error('Error fetching campus list:', error);
      }
    },
    async fetchBuilding() {
      if (this.form.campus) {
        try {
          const response = await axios.get(`${backendUrl}campus/${this.form.campus}`);
          this.buildingList = response.data;
        } catch (error) {
          console.error('Error fetching building list:', error);
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

    // async Search() {
    //     try {
    //     axios.get(`${backendUrl}search_spaces/`, {
    //         params: {
    //             campus: this.form.campus,
    //             building: this.form.building,
    //         },
    //     }).then(response => {
    //       console.log("datos", response.data);
    //       this.$router.push("/filteredSpaces");
    //       });
            
    //     } catch (error) {
    //         console.error('Error al realizar la búsqueda:', error.response || error);
    //     }
    // }
  },
};
</script>