<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
      <span style="visibility: hidden;"></span>
      <span></span>
      <span></span>
      <span style="background-color: #787CFF;"></span>
    </div>
    <div class="container mt-3">
      <div class="row">
        <div class="col-md-4 mb-3">
          <button class="btn btn-primary btn-block">
            Buscar Disponibilidad
          </button>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div class="table-container">
            <table class="table">
              <thead>
                <tr>
                  <th>id</th>
                  <th>Nombre</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in spacesItems" :key="index">
                  <td>{{ item.id }}</td>
                  <td>{{ item.name }}</td>
                  <td>{{ item.seat_status }}</td>
                </tr>
              </tbody>
            </table>
          </div>
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
      spacesItems: [],
    };
  },
  mounted() {
    this.listSpaceItems();
  },
  methods: {
    listSpaceItems() {
      const token = localStorage.getItem("token");
      const spaceId = this.$route.params.spaceId;
      if (token) {
        axios
          .get(`${backendUrl}${spaceId}/desk/`, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.spacesItems = response.data;
            console.log("datos: ", response.data);
          })
          .catch((error) => {
            console.error("Error en la obtención de items de espacio:", error);
          });
      } else {
        console.error("No se encontró el token de autenticación.");
      }
    },
  },
};
</script>

<style>
.table-container {
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  overflow: hidden;
}

.table-container table {
  background-color: transparent;
}
</style>
