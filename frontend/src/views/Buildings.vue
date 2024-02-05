<template>
  <div>
    <div class="position-relative">
      <!-- shape Hero -->
      <section class="section-shaped my-0">
        <div class="shape shape-style-3 shape-default shape-skew">
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
        <div class="container shape-container d-flex">
          <link
            href="/assets/vendor/font-awesome/css/font-awesome.min.css"
            rel="stylesheet"
          />
          <div class="col px-0">
            <h1 class="mb-4">Lista de facultades</h1>
            <p class="mb-3" style="color: azure;">Filtra por campus:</p>
            <!-- Selector de campus -->
            <b-form-select
              v-model="selectedCampus"
              :options="campusOptions"
              placeholder="Seleccionar Campus"
              class="mb-3 custom-select"
            ></b-form-select>

            <!-- Lista de edificios -->
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
              <b-card
                v-for="building in filteredBuildings"
                :key="building.id"
                no-body
                class="overflow-hidden mb-4 custom-card"
                style="max-width: 100%;"
              >
                <b-row no-gutters>
                  <b-col md="6">
                    <b-card-img
                      :src="
                        building.image
                          ? getBuildingImageUrl(building.image)
                          : '/img/alternative.jpg'
                      "
                      alt="Building Image"
                      class="rounded-0 custom-img"
                    ></b-card-img>
                  </b-col>
                  <b-col md="6">
                    <b-card-body :title="building.name_complete">
                      <b-card-text>{{ building.address }}</b-card-text>
                      <b-card-text>{{ building.web }}</b-card-text>
                      <router-link
                        :to="{
                          name: 'building-spaces',
                          params: { buildingId: building.id },
                        }"
                      >
                        <b-button variant="primary" class="mt-4"
                          >Ver salas</b-button
                        >
                      </router-link>
                    </b-card-body>
                  </b-col>
                </b-row>
              </b-card>
              <!-- Fin del bucle v-for -->
            </div>
          </div>
        </div>
      </section>
      <!-- 1st Hero Variation -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";
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
