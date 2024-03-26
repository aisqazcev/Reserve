<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
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
      <h1 class="mb-4">
        <span class="icon-arrow-left" @click="goBack"></span>
        {{ building.name_complete }}
      </h1>
      <card class="mb-3">
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
                Información y contacto
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

              <div
                class="d-flex align-items-center"
                style="margin-bottom: 20px;"
              >
                <i
                  class="ni ni-world-2 mr-2"
                  style="font-size: 24px; color:#be0f2e"
                ></i>
                {{ building.web }}
              </div>

              <div
                class="d-flex align-items-center"
                style="margin-bottom: 20px;"
              >
                <i
                  class="ni ni-email-83 mr-2"
                  style="font-size: 24px; color:#be0f2e;"
                ></i>
                {{ building.email }}
              </div>

              <div
                class="d-flex align-items-center"
                style="margin-bottom: 20px;"
              >
                <i
                  class="ni ni-mobile-button mr-2 "
                  style="font-size: 24px; color:#be0f2e;"
                ></i>
                {{ building.phone }}
              </div>
            </div>
          </div>
        </div>
      </card>

      <div class="mb-5"></div>

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
                      class="img-fluid rounded-square"
                      alt="Imagen del espacio"
                    />
                  </div>

                  <h5 :class="space.name">{{ space.name }}</h5>
                  <div class="d-flex align-items-center icon-container">
                    <equipment :equipments="space.features" :show-equipment-names="false"></equipment>
                  </div>
                  <div class="progress-label mt-4">
                    <span
                      >Ocupación actual
                      <strong>{{ space.occupation }}%</strong></span
                    >
                  </div>

                  <div class="progress mt-4" style="height: 8px;">
                    <div
                      role="progressbar"
                      aria-valuenow="occupation"
                      aria-valuemin="0"
                      aria-valuemax="100"
                      class="progress-bar bg-primary"
                      :style="{ width: space.occupation + '%' }"
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
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";
import Card from "../components/Card.vue";
import "@fortawesome/fontawesome-free/css/all.css";
import Equipment from "../components/Equipment.vue";

export default {
  components: { Equipment, Card },
  data() {
    return {
      building: {},
      spaces: [],
      buildingId: null,
      freeSeats: null,
      occupation: 0,
      campus: {},
    };
  },
  mounted() {
    this.buildingId = this.$route.params.buildingId || "";
    this.fetchSpaces();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
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
          this.fetchOccupation();
        })
        .catch((error) => {
          console.error("Error fetching spaces:", error);
        });
    },
    getSpaceImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/*/, "");
      relativePath = relativePath.replace(/^media\/*/, "");
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
        for (const spaceIndex in this.spaces) {
          if (this.spaces[spaceIndex]) {
            const spaceId = this.spaces[spaceIndex].id;
            const response = await axios.get(
              `${backendUrl}occupation-actual/${spaceId}`
            );
            const occupationPercentage = response.data.occupationPercentage;

            this.occupation = occupationPercentage;

            this.$set(this.spaces, spaceIndex, {
              ...this.spaces[spaceIndex],
              occupation: occupationPercentage,
            });
          } else {
            console.error(
              `El espacio en el índice ${spaceIndex} no está definido.`
            );
          }
        }
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
.icon-container {
  height: 50px; 
}

.icon-container equipment {
  width: 50px; 
  height: 50px;
  margin-right: 10px;
}
</style>
