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
          <link href="/assets/vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet">
          <div class="col px-0">
            <div class="row">
              <div class="col-lg-6">
                <h1 class="display-3  text-white mb-2">{{ building.name_complete }}</h1>
                <div class="d-flex align-items-center mb-3">
                <i class="ni ni-square-pin mr-2" style="font-size: 24px; color:white;"></i>
                <p class="text-white mb-0">{{ building.address }}</p>
                </div>
                <div class="d-flex align-items-center mb-3">
                <i class="ni ni-world-2 mr-2" style="font-size: 24px; color:white;"></i>
                <p class="text-white mb-0">{{ building.web }}</p>
                </div>
                <div class="d-flex align-items-center mb-3">
                <i class="ni ni-email-83 mr-2" style="font-size: 24px; color:white;"></i>
                <p class="text-white mb-0">{{ building.email }}</p>
                </div>
                <div class="d-flex align-items-center mb-3">
                <i class="ni ni-mobile-button mr-2" style="font-size: 24px; color:white;"></i>
                <p class="text-white mb-0">{{ building.phone }}</p>
                </div>
                <p class="text-white">Servicios: {{ building.services }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!-- 1st Hero Variation -->
    </div>
    <section class="section section-lg pt-lg-0 mt--200">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-12">
            <div class="row row-grid">
              <!-- Utiliza v-for para iterar sobre cada espacio -->
              <div v-for="space in spaces" :key="space.id" class="col-lg-4 col-md-6 mb-4">
                <card class="border-0" hover shadow body-classes="py-5">
                  <div class="square-frame">
                    <img
                    :src="space.image ? getSpaceImageUrl(space.image)  : '/img/alternative.jpg'"
                      class="img-fluid shadow-lg mb-4 rounded-square"
                      alt="Imagen del espacio"
                    />
                  </div>
                  <h5 :class="space.name">{{ space.name }}</h5>
                  <p class="description mt-3">{{ space.general_info }}</p>
                  <!-- <div>
                    TODO Utiliza v-for para iterar sobre INFO de cada SALA 
                    <badge
                      v-for="badge in space.badges"
                      :type="badge.type"
                      :rounded="badge.rounded"
                      >{{ badge.label }}</badge
                    >
                  </div> -->
                  <!--TODO Redireccionar a la página de detalles de la sala -->
                  <router-link :to="`/${space.id}/desk`">
                    <base-button type="primary" class="mt-4">
                      Ver detalles
                    </base-button>
                  </router-link>
                </card>
              </div>
              <!-- Fin del bucle v-for -->
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

export default {
  data() {
    return {
      building: {},
      spaces: [],
      buildingId: null,
    };
  },
  mounted() {
    this.buildingId = this.$route.params.buildingId || '';
    // Luego, llamar a fetchSpaces
    this.fetchSpaces();
  },
  methods: {
    async fetchSpaces() {
      console.log("backendUrl:", backendUrl);

      await axios
        .get(`${backendUrl}building/${this.buildingId}/`)
        .then((response) => {
          this.building = response.data;
          console.log("building", this.building);
        })
        .catch((error) => {
          console.error("Error fetching building details:", error);
        });

      await axios
        .get(`${backendUrl}building/${this.buildingId}/spaces/`)
        .then((response) => {
          this.spaces = response.data;
          console.log("spaces", this.spaces);
        })
        .catch((error) => {
          console.error("Error fetching spaces:", error);
        });
    },
    getSpaceImageUrl(relativePath) {
      // Construir la URL completa de la imagen utilizando la URL del backend
      const imageUrl = `${backendUrl}${relativePath}`;
    console.log('URL de la imagen completa:', imageUrl);
    return imageUrl;
    },
  }, 
  computed: {
      get() {
        return this.$route.params.buildingId;
      },    
  },
  watch: {
    '$route'(to, from) {
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
  width: 150px; /* Ajusta el ancho según tus necesidades */
  height: 150px; /* Ajusta la altura según tus necesidades */
  overflow: hidden;
  position: relative;
}

.square-frame img {
  width: 100%;
  height: auto;
}

.rounded-square {
  border-radius: 10px; /* Ajusta el radio según tus necesidades */
}
</style>
