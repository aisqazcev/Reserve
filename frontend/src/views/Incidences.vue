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
          <h3 class="card-title">Formulario de Incidencia</h3>
          <form @submit.prevent="sendIncidence" role="form">
            <div class="row">
              <div class="col-sm-6">
                <div class="form-group">
                  <label for="equipment" style="color: black"
                    >Equipamiento Afectado</label
                  >
                  <select
                    v-model="formData.equipment"
                    id="equipment"
                    class="form-control"
                  >
                    <option value="">Seleccionar equipamiento</option>
                    <option
                      v-for="equipment in equipmentList"
                      :key="equipment.id"
                      :value="equipment.id"
                      >{{ equipment.name }}</option
                    >
                  </select>
                </div>
                <div class="form-group">
                  <label for="campusType" style="color: black">Campus</label>
                  <select
                    v-model="selectedCampus"
                    class="form-control"
                    id="campusType"
                  >
                    <option :value="null">Seleccionar campus</option>
                    <option
                      v-for="campus in campuses"
                      :key="campus.id"
                      :value="campus.id"
                      >{{ campus.campus_name }}</option
                    >
                  </select>
                </div>
                <div class="form-group">
                  <label for="buildingType" style="color: black"
                    >Edificio</label
                  >
                  <select
                    v-model="selectedBuilding"
                    class="form-control"
                    id="buildingType"
                  >
                    <option :value="null">Seleccionar edificio</option>
                    <option
                      v-for="building in filteredBuildings"
                      :key="building.id"
                      :value="building.id"
                      >{{ building.name_complete }}</option
                    >
                  </select>
                </div>
                <div class="form-group">
                  <label for="spaceType" style="color: black">Sala</label>
                  <select
                    v-model="selectedSpace"
                    class="form-control"
                    id="spaceType"
                  >
                    <option :value="null">Seleccionar sala</option>
                    <option
                      v-for="space in filteredSpaces"
                      :key="space.id"
                      :value="space.id"
                      >{{ space.name }}</option
                    >
                  </select>
                </div>
                <div class="form-group">
                  <label for="deskType" style="color: black">Asiento</label>
                  <select
                    v-model="selectedDesk"
                    class="form-control"
                    id="deskType"
                    :disabled="!selectedSpace"
                  >
                    <option :value="null">Seleccionar asiento</option>
                    <option
                      v-for="desk in filteredDesks"
                      :key="desk.id"
                      :value="desk.id"
                      >{{ desk.name }}</option
                    >
                  </select>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="form-group">
                  <label for="title" style="color: black">Título</label>
                  <input
                    v-model="formData.title"
                    type="text"
                    id="title"
                    class="form-control"
                    placeholder="Introduce el título de la incidencia"
                  />
                </div>
                <div class="form-group">
                  <label for="description" style="color: black"
                    >Descripción</label
                  >
                  <textarea
                    v-model="formData.description"
                    id="description"
                    class="form-control"
                    rows="3"
                    style="height: 325px;"
                    placeholder="Introduce la descripción de la incidencia"
                  ></textarea>
                </div>
              </div>
            </div>
            <div class="row mt-3">
              <div
                class="col-sm d-flex flex-column align-items-center justify-content-center"
              >
                <button
                  :disabled="loading"
                  type="submit"
                  class="btn btn-primary my-4"
                >
                  Enviar incidencia
                </button>
                <div
                  v-if="errorMessage"
                  class="alert alert-danger mt-3"
                  role="alert"
                >
                  <i class="fas fa-exclamation-triangle"></i>
                  {{ errorMessage }}
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";

export default {
  data() {
    return {
      formData: {
        title: "",
        description: "",
        equipment: "",
      },
      loading: false,
      errorMessage: "",
      equipmentList: [],
      selectedCampus: null,
      selectedBuilding: null,
      selectedSpace: null,
      selectedDesk: null,
      campuses: [],
      buildings: [],
      spaces: [],
      desks: [],
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
    filteredSpaces() {
      if (this.selectedBuilding) {
        return this.spaces.filter(
          (space) => space.building === this.selectedBuilding
        );
      }
      return this.spaces;
    },
    filteredDesks() {
      if (this.selectedSpace) {
        return this.desks.filter(
          (desk) => desk.space_id === this.selectedSpace
        );
      }
      return this.desks;
    },
  },
  watch: {
    selectedSpace(newVal, oldVal) {
      if (newVal !== null) {
        this.loadDesks();
      }
    },
  },
  mounted() {
    this.loadEquipment();
    this.loadCampuses();
    this.loadBuildings();
    this.loadSpaces();
  },
  methods: {
    loadEquipment() {
      axios
        .get(`${backendUrl}equipment/`)
        .then((response) => {
          this.equipmentList = response.data;
        })
        .catch((error) => {
          console.error("Error al obtener la lista de equipos:", error);
        });
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
    async loadSpaces() {
      try {
        if (this.selectedBuilding === null) {
          const response = await axios.get(`${backendUrl}spaces/`);
          this.spaces = [...response.data];
        } else {
          const response = await axios.get(
            `${backendUrl}buildings/?campus_id=${this.selectedCampus}/spaces`
          );
          this.spaces = response.data;
          this.spaces.unshift({ id: null, name: "Cualquiera" });
          this.loadDesks();
        }
      } catch (error) {
        console.error("Error fetching buildings:", error);
      }
    },
    async loadDesks() {
      try {
        const response = await axios.get(
          `${backendUrl}${this.selectedSpace}/desk/`
        );
        this.desks = response.data;
        console.log("Desks: ", this.desks);
        this.desks.unshift({ id: null, name: "Cualquiera" });
      } catch (error) {
        console.error("Error fetching buildings:", error);
      }
    },
    sendIncidence() {
      if (
        !this.formData.title ||
        !this.formData.description ||
        !this.formData.equipment ||
        !this.selectedCampus ||
        !this.selectedBuilding ||
        !this.selectedSpace
      ) {
        this.errorMessage =
          "Es necesario completar todos los campos excepto el Asiento.";
        return;
      }
      const subject = this.formData.title;
      const message = this.formData.description;
      const equipment = this.formData.equipment;
      const campus = this.selectedCampus;
      const building = this.selectedBuilding;
      const space = this.selectedSpace;
      const desk = this.selectedDesk;
      axios
        .post(
          `${backendUrl}send_incidence/`,
          {
            subject: subject,
            message: message,
            equipment: equipment,
            campus: campus,
            building: building,
            space: space,
            desk: desk,
          }
        )
        .then((response) => {
          this.formData.title = "";
          this.formData.description = "";
          this.formData.equipment = "";
          this.selectedCampus = null;
          this.selectedBuilding = null;
          this.selectedSpace = null;
          this.selectedDesk = null;
        })
        .catch((error) => {
          console.error("Error al enviar el correo electrónico:", error);
        });
    },
  },
};
</script>
