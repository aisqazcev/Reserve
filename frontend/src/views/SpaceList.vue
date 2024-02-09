<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
      <span style="visibility: hidden;"></span>
      <span></span>
      <span></span>
      <span style="background-color: #787CFF;"></span>
    </div>
    <div class="container mt-3">
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-md-4 mb-3">
              <div class="form-group">
                <label for="fecha">Fecha:</label>
                <input type="date" id="date" class="form-control" />
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="form-group">
                <label for="horaInicio">Hora de inicio:</label>
                <input type="time" id="start_time" class="form-control" />
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="form-group">
                <label for="duracion">Duración (minutos):</label>
                <input type="number" id="duration" class="form-control" />
              </div>
            </div>
            <div class="col-md-12">
              <button class="btn btn-primary btn-block" @click="buscarDisponibilidad">
                Buscar Disponibilidad
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="row mt-3">
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
    buscarDisponibilidad() {
      const date = document.getElementById("date").value;
      const start_time = document.getElementById("start_time").value;
      const duration = document.getElementById("duration").value;

      console.log("Fecha:", date);
      console.log("Hora de inicio:", start_time);
      console.log("Duración:", duration);

      // Hacer la solicitud al backend
      axios
  .get(`${backendUrl}find-available-seats/`, {
    params: {
      start_time: `${date} ${start_time}`,
      duration: duration,
    },
  })
  .then((response) => {
    // Actualizar la vista con los resultados recibidos
    this.spacesItems = response.data.available_seats.map((id) => ({
      id: id,
      name: "",
      seat_status: "AVAILABLE",
    }));
  })
  .catch((error) => {
    console.error("Error al buscar disponibilidad:", error);
  });

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
