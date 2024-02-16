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
            <div class="text-center text-muted mb-4">
              <small>Buscar Disponibilidad de Espacios</small>
            </div>
            <form @submit.prevent="buscarDisponibilidad" role="form">
              <base-input
                alternative
                type="date"
                placeholder="Fecha"
                v-model="selectedDate"
              ></base-input>

              <base-input
                alternative
                type="time"
                placeholder="Hora"
                v-model="selectedTime"
              ></base-input>

              <base-input
                alternative
                type="number"
                placeholder="Duración (minutos)"
                v-model="selectedDuration"
                min="1"
              ></base-input>

              <div class="form-group">
                <label for="campusType">Campus</label>
                <select
                  v-model="selectedCampus"
                  class="form-control"
                  id="campusType"
                >
                  <option :value="null">Cualquier campus</option>
                  <option
                    v-for="campus in campuses"
                    :key="campus.id"
                    :value="campus.id"
                    >{{ campus.campus_name }}</option
                  >
                </select>
              </div>

              <div class="form-group" v-if="selectedCampus !== null">
                <label for="buildingType">Facultad</label>
                <select
                  v-model="selectedBuilding"
                  class="form-control"
                  id="buildingType"
                >
                  <option :value="null">Seleccionar Facultad</option>
                  <option
                    v-for="building in filteredBuildings"
                    :key="building.id"
                    :value="building.id"
                    >{{ building.name }}</option
                  >
                </select>
              </div>

              <div class="text-center">
                <base-button
                  :disabled="loading"
                  type="primary"
                  class="my-4"
                  @click="buscarDisponibilidad"
                >
                  Buscar Disponibilidad
                </base-button>
              </div>
            </form>
            <div v-if="spaces.length > 0">
              <h3>Salas Disponibles</h3>
              <ul>
                <li v-for="space in spaces" :key="space.id">
                  {{ space.name }}
                </li>
              </ul>
            </div>
          </card>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  name: "booking",
  data() {
    return {
      selectedDate: "",
      selectedTime: "",
      selectedCampus: null,
      selectedBuilding: null,
      selectedDuration: 60,
      campuses: [],
      buildings: [],
      spaces: [],
    };
  },
  computed: {
    filteredBuildings() {
      if (this.selectedCampus) {
        // Filtrar los edificios por el ID del campus seleccionado
        return this.buildings.filter(
          (building) => building.campus === this.selectedCampus
        );
      }
      // Si no se ha seleccionado un campus, devolver todos los edificios
      return this.buildings;
    },
  },
  mounted() {
    this.loadCampuses();
    this.loadBuildings(); // Cargar todos los edificios al inicio
  },
  methods: {
    async loadCampuses() {
      axios
        .get(`${backendUrl}campuses/`)
        .then((response) => {
          this.campuses = response.data;
        })
        .catch((error) => {
          console.error("Error fetching campuses:", error);
        });
    },
    async loadBuildings() {
      axios
        .get(`${backendUrl}buildings/`)
        .then((response) => {
          // Asignar todos los edificios a la propiedad buildings
          this.buildings = response.data;
        })
        .catch((error) => {
          console.error("Error fetching buildings:", error);
        });
    },
    buscarDisponibilidad() {
      axios
        .get(`${backendUrl}find-available-spaces/`, {
          params: {
            date: this.selectedDate,
            start_time: this.selectedTime,
            duration: this.selectedDuration,
            campus_id: this.selectedCampus,
            building_id: this.selectedBuilding,
          },
        })
        .then((response) => {
          this.spaces = response.data;
        })
        .catch((error) => {
          console.error("Error al buscar disponibilidad:", error);
        });
    },
  },
};
</script>
