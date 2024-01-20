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
          <div class="col px-0">
            <div class="row">
              <div class="col-lg-6">
                <h1 class="display-3  text-white">{{buildingName}}</h1>
                <ul>
                  <li v-for="space in spaces" :key="space.id">
                    {{ space.name }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        </section>
                    <!-- 1st Hero Variation -->
    </div>
        <section
          class="section section-lg pt-lg-0 mt--200">
          <div class="container">
            <div class="row justify-content-center">
              <div class="col-lg-12">
                <div class="row row-grid">
                  <!-- Utiliza v-for para iterar sobre cada espacio -->
                  <div v-for="space in spaces" :key="space.id" class="col-lg-4">
                    <card class="border-0" hover shadow body-classes="py-5">
                      <icon
                        name="ni ni-check-bold"
                        type="primary"
                        rounded
                        class="mb-4"
                      >
                      </icon>
                      <h5 :class="space.name">{{ space.name }}</h5>
                      <p class="description mt-3">{{ space.general_info }}</p>
                      <div>
                        <!-- TODO Utiliza v-for para iterar sobre INFO de cada SALA -->
                        <badge
                          v-for="badge in space.badges"
                          :type="badge.type"
                          :rounded="badge.rounded"
                          >{{ badge.label }}</badge
                        >
                      </div>
                      <!--TODO Redireccionar a la página de detalles de la sala -->
                      <base-button tag="a" href="#" type="primary" class="mt-4">
                        Ver detalles
                      </base-button>
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
      spaces: [],
      buildingName: "",
    };
  },
  // computed: {
  //   buildingName() {
  //     return this.$route.params.buildingName;
  //   },
  // },
  // watch: {
  //   buildingName: "fetchSpaces",
  // },
  mounted() {
    // Asignar un valor inicial a buildingName
    this.buildingName = this.$route.params.buildingName || '';
    // Luego, llamar a fetchSpaces
    this.fetchSpaces();
  },
  methods: {
    async fetchSpaces() {
      try {
        const response = await axios.get(
          `${backendUrl}building/${this.buildingName}/spaces/`
        );
        this.spaces = response.data;

        // Verificar si hay espacios
        if (this.spaces.length > 0) {
          // Obtener el nombre del edificio desde el primer espacio
          this.buildingName = this.spaces[0].building.name_complete;
          console.log("Lista de espacios", this.spaces);
        } else {
          // En caso de que no haya espacios, establecer el nombre del edificio como vacío o algún valor predeterminado
          this.buildingName = "Nombre no disponible";
        }
      } catch (error) {
        console.error("Error al cargar la lista de espacios", error);
      }
    },
  },
};
</script>
