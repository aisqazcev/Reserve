<template>
  <section class="section-shaped my-0 d-flex ">
    <div class="shape shape-style-3 shape-default ">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container mt-3">
      <div class="col px-0">
        <h1 class="mb-4">Lista de facultades</h1>
        <p class="mb-3" style="color: azure;">Filtra por campus:</p>
        <b-form-select
          v-model="selectedCampus"
          :options="campusOptions"
          placeholder="Seleccionar Campus"
          class="mb-3 custom-select"
        ></b-form-select>
        <div class="row">
          <div class="col-md-12 mb-4">
            <div v-for="building in filteredBuildings" :key="building.id" class="mb-4">
              <card class="custom-card">
                <div class="row">
                  <div class="col-md-5">
                    <img
                      :src="
                        building.image
                          ? getBuildingImageUrl(building.image)
                          : '/img/alternative.jpg'
                      "
                      class="img-fluid shadow-lg mb-4 rounded-square"
                      alt="Imagen del espacio"
                    />
                  </div>
                  <div class="col-md-7">
                    <div class="card-body-1">
                      <h3 class="card-title">
                        {{ building.name_complete }}
                      </h3>
                      <div
                        class="d-flex align-items-center"
                        style="margin-bottom: 20px;"
                      >
                        <i
                          class="ni ni-square-pin mr-2"
                          style="font-size: 24px; color:#be0f2e;"
                        ></i>
                        {{ building.address }}
                      </div>
                      <router-link :to="`/building/${building.id}`">
                        <b-button variant="primary" class="mt-4"
                          >Ver detalles</b-button
                        >
                      </router-link>
                    </div>
                  </div>
                </div>
              </card>
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
      buildings: [],
      campuses: [],
      selectedCampus: null,
    };
  },
  computed: {
    campusOptions() {
      const allCampusesOption = { text: "Todas las facultades", value: null };

      const campusOptions = [
        allCampusesOption,
        ...this.campuses.map((campus) => ({
          text: campus.campus_name,
          value: campus.id,
        })),
      ];

      return campusOptions;
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
    this.fetchCampuses();
    this.fetchBuildings();
  },
  methods: {
    async fetchCampuses() {
      try {
        const response = await axios.get(`${backendUrl}campuses/`);
        this.campuses = response.data;
      } catch (error) {
        console.error("Error al cargar la lista de campus", error);
      }
    },

    async fetchBuildings() {
      try {
        const response = await axios.get(`${backendUrl}buildings/`);
        this.buildings = response.data;
      } catch (error) {
        console.error("Error al cargar la lista de edificios", error);
      }
    },

    getBuildingImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/*/, "");
      relativePath = relativePath.replace(/^media\//, "");
      const imageUrl = `${backendUrl}${relativePath}`;
      return imageUrl;
    },
  },
};
</script>
<style>
.custom-select {
  width: 300px !important;
}
</style>
