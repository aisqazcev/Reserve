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
      <div class="card mb-3 text-white">
        <div class="card-body">
          <h3 class="card-title">Buscar Disponibilidad de Espacios</h3>
          <form @submit.prevent="buscarDisponibilidad" role="form">
            <div class="ct-example-row">
              <div class="row">
                <div class="col-sm">
                  <label for="date" style="color: black">Fecha</label>
                  <base-input
                    alternative
                    type="date"
                    v-model="selectedDate"
                    id="date"
                  ></base-input>
                </div>
                <div class="col-sm">
                  <label for="time" style="color: black">Hora</label>
                  <base-input
                    alternative
                    type="time"
                    v-model="selectedTime"
                    id="time"
                  ></base-input>
                </div>
                <div class="col-sm">
                  <label for="duracion" style="color: black">Duración:</label>
                  <select
                    id="duration"
                    v-model="selectedDuration"
                    class="form-control"
                    @change="handleDurationChange"
                  >
                    <option value="15">0:15</option>
                    <option value="30">0:30</option>
                    <option value="45">0:45</option>
                    <option value="60">1:00</option>
                    <option value="75">1:15</option>
                    <option value="90">1:30</option>
                    <option value="105">1:45</option>
                    <option value="120">2:00</option>
                    <option value="135">2:15</option>
                    <option value="150">2:30</option>
                    <option value="165">2:45</option>
                    <option value="180">3:00</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-sm-6">
                  <label for="campusType" style="color: black">Campus</label>
                  <select
                    v-model="selectedCampus"
                    class="form-control"
                    id="campusType"
                  >
                    <option :value="null">Cualquiera</option>
                    <option
                      v-for="campus in campuses"
                      :key="campus.id"
                      :value="campus.id"
                    >
                      {{ campus.campus_name }}
                    </option>
                  </select>
                </div>
                <div class="col-sm-6">
                  <label for="buildingType" style="color: black"
                    >Facultad</label
                  >
                  <select
                    v-model="selectedBuilding"
                    class="form-control"
                    id="buildingType"
                  >
                    <option :value="null">Cualquiera</option>
                    <option
                      v-for="building in filteredBuildings"
                      :key="building.id"
                      :value="building.id"
                    >
                      {{ building.name_complete }}
                    </option>
                  </select>
                </div>
                <div
                  class="col-sm d-flex flex-column align-items-center justify-content-center"
                >
                  <base-button
                    :disabled="loading"
                    type="primary"
                    class="my-4"
                    @click="buscarDisponibilidad"
                  >
                    Buscar Disponibilidad
                  </base-button>
                  <div
                    v-if="errorMessage"
                    class="alert alert-default error-message mt-3"
                    role="alert"
                  >
                    <i class="fas fa-exclamation-triangle"></i>
                    {{ errorMessage }}
                  </div>
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
              <div class="card-body-1">
                <h3 style="font-size: 24px">
                  {{ space.building.campusName }}
                  <i class="ni ni-bold-right"></i>
                  {{ space.building.name_complete }}
                  <i class="ni ni-bold-right"></i>
                  {{ space.name }}
                </h3>
                <div class="d-flex align-items-center">
                  <i
                    class="ni ni-square-pin"
                    style="
                      font-size: 24px;
                      color: #be0f2e;
                      margin-right: 15px;
                      margin-top: 30px;
                    "
                  ></i>
                  <h6 style="margin-top: 30px">
                    {{ space.building.address }}
                  </h6>
                </div>
                <router-link
                  :to="{
                    path: `/space/${space.id}`,
                    query: {
                      date: selectedDate,
                      time: selectedTime,
                      duration: selectedDuration,
                    },
                  }"
                >
                  <b-button
                    variant="primary"
                    class="mt-0 float-right"
                    style="margin-right: 15px"
                    >Reservar asiento</b-button
                  >
                </router-link>
              </div>
            </div>
          </card>
        </div>
      </div>
      <div v-if="search && spaces.length == 0" class="mt-4">
        <div class="alert alert-danger" role="alert">
          Lo sentimos, no se han encontrado sitios disponibles para esa
          configuración.
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
    const now = new Date();
    const currentDate = now.toISOString().substring(0, 10);
    now.setMinutes(0, 0, 0);
    now.setHours(now.getHours() + 1);
    let hours = now.getHours().toString().padStart(2, "0");
    let minutes = now.getMinutes().toString().padStart(2, "0");
    const nextHour = `${hours}:${minutes}`;

    return {
      selectedDate: currentDate,
      selectedTime: nextHour,
      errorMessage: "",
      selectedCampus: null,
      selectedBuilding: null,
      selectedDuration: 60,
      campuses: [],
      buildings: [],
      spaces: [],
      loading: false,
      search: false,
    };
  },
  watch: {
    async selectedCampus(newCampus) {
      if (newCampus !== null) {
        await this.loadBuildings();

        if (this.selectedBuilding !== null) {
          this.selectedBuilding = null;
        }
      } else {
        await this.loadBuildings();
      }
    },
  },
  computed: {
    formattedDuration() {
      const hours = Math.floor(this.selectedDuration / 60);
      const minutes = this.selectedDuration % 60;
      return `${hours}:${minutes.toString().padStart(2, "0")}`;
    },
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
    handleDurationChange(event) {},
    toggleReadOnly() {},
    isPastDate(dateString) {
      const selectedDate = new Date(dateString);
      const currentDate = new Date();
      currentDate.setHours(0, 0, 0, 0);
      return selectedDate < currentDate;
    },

    isPastTime(timeString) {
      const currentTime = new Date();
      const [hours, minutes] = timeString.split(":");
      const selectedTime = new Date();
      selectedTime.setHours(hours, minutes, 0, 0);

      return selectedTime < currentTime;
    },

    getCurrentDate() {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, "0");
      const day = String(currentDate.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    },

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
      try {
        if (this.selectedCampus === null) {
          const response = await axios.get(`${backendUrl}buildings/`);
          this.buildings = [...response.data];
        } else {
          const response = await axios.get(
            `${backendUrl}buildings/?campus_id=${this.selectedCampus}`
          );
          this.buildings = response.data;
          this.buildings.unshift({ id: null, name_complete: "Cualquiera" });
        }
      } catch (error) {
        console.error("Error fetching buildings:", error);
      }
    },
    getSpaceImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/*/, "");
      const imageUrl = `${backendUrl}${relativePath}`;
      return imageUrl;
    },
    buscarDisponibilidad() {
      this.errorMessage = "";
      if (!this.selectedDate || !this.selectedTime || !this.selectedDuration) {
        this.errorMessage =
          "Por favor, complete los campos fecha, hora y duración.";
        return;
      }
      if (this.isPastDate(this.selectedDate)) {
        this.errorMessage = "No se puede seleccionar una fecha pasada.";
        return;
      }
      if (
        this.selectedDate == this.getCurrentDate() &&
        this.isPastTime(this.selectedTime)
      ) {
        this.errorMessage =
          "No se puede seleccionar una hora anterior a la hora actual para el día de hoy.";
        return;
      }
      this.search = true;

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
          const availableSpaceIds = response.data.available_spaces;
          const spacesDetails = await Promise.all(
            availableSpaceIds.map(async (spaceId) => {
              const spaceResponse = await axios.get(
                `${backendUrl}space/${spaceId}/`
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
<style scoped>
.readonly-input {
  position: relative;
}

.readonly-input input {
  pointer-events: none;
}

.readonly-input::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: not-allowed;
}
</style>
