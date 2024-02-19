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
      <div class="card mb-3  text-white">
        <div class="card-body">
          <h3 class="card-title" style="color: #08217E;">
            Buscar Disponibilidad de Espacios
          </h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="buscarDisponibilidad" role="form">
            <div class="ct-example-row">
              <div class="row">
                <div class="col-sm">
                  <base-input
                    alternative
                    type="date"
                    placeholder="Fecha"
                    v-model="selectedDate"
                  ></base-input>
                </div>
                <div class="col-sm">
                  <base-input
                    alternative
                    type="time"
                    placeholder="Hora"
                    v-model="selectedTime"
                  ></base-input>
                </div>
                <div class="col-sm">
                  <base-input
                    alternative
                    type="number"
                    placeholder="Duración (minutos)"
                    v-model="selectedDuration"
                    min="15"
                  ></base-input>
                </div>
              </div>
              <div class="row">
                <div class="col-sm-6">
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
                <div class="col-sm-6">
                  <label for="buildingType">Facultad</label>
                  <select
                    v-model="selectedBuilding"
                    class="form-control"
                    id="buildingType"
                    :disabled="selectedCampus === null"
                  >
                    <option :value="null" :disabled="selectedCampus == null"
                      >Cualquier Facultad</option
                    >
                    <option
                      v-for="building in filteredBuildings"
                      :key="building.id"
                      :value="building.id"
                      >{{ building.name_complete }}</option
                    >
                  </select>
                </div>
                <div
                  class="col-sm d-flex justify-content-center align-items-center"
                >
                  <base-button
                    :disabled="loading"
                    type="primary"
                    class="my-4 w-100"
                    @click="buscarDisponibilidad"
                  >
                    Buscar Disponibilidad
                  </base-button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
      <div v-if="spaces.length > 0" class="mt-4">
        <div class="card-body">
          <h5 class="card-title">Espacios con sitios disponibles</h5>
        </div>
        <div v-for="space in spaces" :key="space.id" class="mb-4">
          <card class="custom-card">
            <div class="row">
              <div class="col-md-7">
                <div class="card-body">
                  <h3 class="card-title" style="color: #08217E;">
                    {{ space.building.campusName }}
                    <i
                      class="ni ni-bold-right"
                      style="font-size: 24px; color:#051551"
                    ></i>
                    {{ space.building.name_complete }}
                    <i
                      class="ni ni-bold-right"
                      style="font-size: 24px; color:#051551"
                    ></i>
                    {{ space.name }}
                  </h3>
                  <div
                    class="d-flex align-items-center"
                    style="margin-bottom: 20px;"
                  >
                    <i
                      class="ni ni-square-pin"
                      style="font-size: 24px; color:#08217E"
                    ></i>
                    <strong>{{
                      space.building && space.building.address
                        ? space.building.address
                        : "Dirección no disponible"
                    }}</strong>
                  </div>
                </div>
              </div>
              <div class="col-md-5 d-flex align-items-end justify-content-end">
                <router-link :to="`/space/${space.id}`">
                  <b-button variant="primary" class="mt-4"
                    >Ver detalles</b-button
                  >
                </router-link>
              </div>
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
import "@fortawesome/fontawesome-free/css/all.css";
import {
  BFormSelect,
  BCard,
  BRow,
  BCol,
  BCardImg,
  BCardBody,
  BCardText,
  BButton,
} from "bootstrap-vue";

export default {
  name: "booking",
  components: {
    BFormSelect,
    BCard,
    BRow,
    BCol,
    BCardImg,
    BCardBody,
    BCardText,
    BButton,
  },
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
      loading: false,
    };
  },
  computed: {
    filteredBuildings() {
      if (this.selectedCampus) {
        return this.buildings.filter(
          (building) => building.campus === this.selectedCampus
        );
      }
      return this.buildings;
    },
  },
  mounted() {
    this.loadCampuses();
    this.loadBuildings();
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
          this.buildings = response.data;
        })
        .catch((error) => {
          console.error("Error fetching buildings:", error);
        });
    },
    getSpaceImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/*/, "");
      const imageUrl = `${backendUrl}${relativePath}`;
      return imageUrl;
    },
    buscarDisponibilidad() {
      axios
        .get(`${backendUrl}find-available-spaces/`, {
          params: {
            start_time: `${this.selectedDate} ${this.selectedTime}`,
            duration: this.selectedDuration,
            campus_id: this.selectedCampus,
            building_id: this.selectedBuilding,
          },
        })
        .then(async (response) => {
          console.log(
            "Respuesta de la API de Espacios Disponibles:",
            response.data
          );
          const availableSpaceIds = response.data.available_spaces;
          const spacesDetails = await Promise.all(
            availableSpaceIds.map(async (spaceId) => {
              const spaceResponse = await axios.get(
                `${backendUrl}spaces/${spaceId}/`
              );
              return spaceResponse.data;
            })
          );
          this.spaces = spacesDetails;
          this.getSpaceDetails();
        })
        .catch((error) => {
          console.error("Error al buscar disponibilidad:", error);
        });
    },
    getSpaceDetails() {
      const buildingPromises = [];
      this.spaces.forEach((space) => {
        buildingPromises.push(
          axios.get(`${backendUrl}building/${space.building}/`)
        );
      });
      Promise.all([...buildingPromises])
        .then((responses) => {
          this.spaces.forEach((space, index) => {
            const buildingIndex = index;
            space.building = responses[buildingIndex].data;
            axios
              .get(`${backendUrl}campus/${space.building.campus}/`)
              .then((response) => {
                this.$set(
                  space.building,
                  "campusName",
                  response.data.campus_name
                );
              })
              .catch((error) => {
                console.error("Error obteniendo detalles del campus:", error);
              });
          });
        })
        .catch((error) => {
          console.error("Error obteniendo detalles del edificio:", error);
        });
    },
  },
};
</script>
