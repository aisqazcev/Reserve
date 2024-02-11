<template>
  <div>
    <div class="position-relative">
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
          <div class="row align-items-center">
            <h1 class="mb-4" style="color: #051551;">
              {{ building.name_complete }}
            </h1>
            <card
              class="row align-items-center"
              style="background-color: rgba(159, 216, 197, 0.5); max-width: fit-content;"
            >
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
                  <div class="d-flex flex-column ">
                    <h2 class="mb-4" style="color: #08217E;">
                      Información y contacto
                    </h2>
                    <div class="d-flex mb-4">
                      <i
                        class="ni ni-square-pin mr-2"
                        style="font-size: 24px; color:#08217E"
                      ></i>
                      <p class="text-black mb-0"><b>{{ building.address }}</b></p>
                    </div>
                    <div class="d-flex mb-4">
                      <i
                        class="ni ni-world-2 mr-2"
                        style="font-size: 24px; color:#08217E;"
                      ></i>
                      <p class="text-black mb-0"><b>{{ building.web }}</b></p>
                    </div>
                    <div class="d-flex mb-4">
                      <i
                        class="ni ni-email-83 mr-2"
                        style="font-size: 24px; color:#08217E;"
                      ></i>
                      <p class="text-black mb-0"><b>{{ building.email }}</b></p>
                    </div>
                    <div class="d-flex">
                      <i
                        class="ni ni-mobile-button mr-2"
                        style="font-size: 24px; color:#08217E;"
                      ></i>
                      <p class="text-black mb-0"><b>{{ building.phone }}</b></p>
                    </div>
                  </div>
                </div>
              </div>
            </card>
          </div>
        </div>
      </section>
    </div>
    <section class="section section-lg pt-lg-0 mt--200">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-12">
            <div class="row row-grid">
              <div
                v-for="space in spaces"
                :key="space.id"
                class="col-lg-4 col-md-6 mb-4"
              >
                <card class="border-0" hover shadow body-classes="py-5">
                  <div class="square-frame">
                    <img
                      :src="
                        space.image
                          ? getSpaceImageUrl(space.image)
                          : '/img/alternative.jpg'
                      "
                      class="img-fluid shadow-lg mb-4 rounded-square"
                      alt="Imagen del espacio"
                    />
                  </div>
                  <h5 :class="space.name">{{ space.name }}</h5>
                  <div class="progress-label mt-4">
                    <span
                      >Ocupación actual <strong>{{ occupation }}%</strong></span
                    >
                  </div>
                  <div class="progress mt-4" style="height: 8px;">
                    <div
                      role="progressbar"
                      aria-valuenow="occupation"
                      aria-valuemin="0"
                      aria-valuemax="100"
                      class="progress-bar bg-primary"
                      :style="{ width: occupation + '%' }"
                    ></div>
                  </div>

                  <router-link :to="`/space/${space.id}`">
                    <base-button type="primary" class="mt-4">
                      Ver detalles
                    </base-button>
                  </router-link>
                </card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";
import Card from "../components/Card.vue";

export default {
  components: { Card },
  data() {
    return {
      building: {},
      spaces: [],
      buildingId: null,
      freeSeats: null,
    };
  },
  mounted() {
    this.buildingId = this.$route.params.buildingId || "";
    this.fetchSpaces();
    this.fetchOccupation();
  },
  methods: {
    async fetchSpaces() {
      await axios
        .get(`${backendUrl}building/${this.buildingId}/`)
        .then((response) => {
          this.building = response.data;
        })
        .catch((error) => {
          console.error("Error fetching building details:", error);
        });

      await axios
        .get(`${backendUrl}building/${this.buildingId}/spaces/`)
        .then((response) => {
          this.spaces = response.data;
        })
        .catch((error) => {
          console.error("Error fetching spaces:", error);
        });
    },
    getSpaceImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/*/, "");
      const imageUrl = `${backendUrl}${relativePath}`;
      return imageUrl;
    },
    getBuildingImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/*/, "");
      relativePath = relativePath.replace(/^media\//, "");
      const imageUrl = `${backendUrl}${relativePath}`;
      return imageUrl;
    },
    async fetchOccupation() {
      try {
        const response = await axios.get(`${backendUrl}occupation-actual/`);
        const occupationPercentage = response.data.occupationPercentage;
        console.log("Ocupacion", response.data);
        console.log("Ocupacion %", occupationPercentage);
        this.occupation = occupationPercentage;
      } catch (error) {
        console.error("Error al obtener la ocupación:", error);
      }
    },
  },
  computed: {
    get() {
      return this.$route.params.buildingId;
    },
  },
  watch: {
    $route(to, from) {
      if (to.params && to.params.buildingId) {
        this.buildingId = to.params.buildingId;
        this.fetchSpaces();
      }
    },
  },
};
</script>
<style>
.square-frame {
  width: 150px;
  height: 150px;
  overflow: hidden;
  position: relative;
}

.square-frame img {
  width: 100%;
  height: auto;
}

.rounded-square {
  border-radius: 5px;
}
</style>
