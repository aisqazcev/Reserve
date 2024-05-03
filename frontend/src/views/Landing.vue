<template>
  <div>
    <div class="position">
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
          <span></span>
        </div>
        <div class="container shape-container d-flex">
          <div class="col px-0">
            <div class="row">
              <div class="col-lg-6">
                <h1 class="display-3">
                  ¡No te quedes sin tu sitio!
                  <span>Reserva asientos</span>
                </h1>
                <p class="lead">
                  Con esta plataforma aseguras tu sitio en el momento y lugar
                  que prefieras. De esta forma evitarás desplazarte y quedarte
                  sin hueco. Además, puedes consultar la ocupación en tiempo
                  real, así como la información de cada espacio.
                </p>
              </div>
              <div class="col-lg-6 mt-4">
                <b-carousel id="carousel1" controls indicators>
                  <b-carousel-slide
                    v-for="(imagen, index) in randomImages"
                    :key="index"
                    :img-src="getSpaceImageUrl(imagen)"
                    class="carousel-image"
                  ></b-carousel-slide>
                </b-carousel>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-12">
                <booking />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";
import "bootstrap/dist/css/bootstrap.css";
import { BCarousel, BCarouselSlide } from "bootstrap-vue";
import Card from "../components/Card.vue";
import Booking from "./Booking.vue";

export default {
  components: {
    BCarousel,
    BCarouselSlide,
    Card,
    Booking,
  },
  data() {
    return {
      randomImages: [],
    };
  },
  methods: {
    getSpaceImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/*/, "");
      relativePath = relativePath.replace(/^media\/*/, "");
      const imageUrl = `${backendUrl}${relativePath}`;
      return imageUrl;
    },
  },
  mounted() {
    axios
      .get(`${backendUrl}get-random-images/`)
      .then((response) => {
        this.randomImages = response.data.urls_imagenes;
      })
      .catch((error) => {
        console.error("Error al obtener imágenes aleatorias:", error);
      });
  },
};
</script>

<style>
.carousel-image img {
  max-width: 100%;
  height: auto;
  max-height: 220px;
}

@media (max-width: 768px) {
  .carousel-image img {
    max-height: 150px;
  }
}
</style>
