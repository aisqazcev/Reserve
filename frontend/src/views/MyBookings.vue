<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
      <span style="visibility: hidden;"></span>
      <span></span>
      <span></span>
      <span style="background-color: #787CFF;"></span>
    </div>
    <div class="container mt-3">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>id</th>
              <th>Fecha</th>
              <th>Inicio</th>
              <th>Duración</th>
              <th>Campus</th>
              <th>Facultad</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in displayedBookings" :key="index">
              <td>{{ item.id }}</td>
              <td>{{ item.date }}</td>
              <td>{{ item.start_time }}</td>
              <td>{{ item.end_time }}</td>
              <td>{{ item.campus }}</td>
              <td>{{ item.building }}</td>
              <td class="td-actions text-right">
                <button
                  type="button"
                  rel="tooltip"
                  class="btn btn-info btn-icon btn-sm"
                  data-original-title=""
                  title=""
                >
                  <i class="ni ni-circle-08 pt-1"></i>
                </button>
                <button
                  type="button"
                  rel="tooltip"
                  class="btn btn-success btn-icon btn-sm"
                  data-original-title=""
                  title=""
                >
                  <i class="fa fa-pencil pt-1"></i>
                </button>
                <button
                  type="button"
                  rel="tooltip"
                  class="btn btn-danger btn-icon btn-sm"
                  data-original-title=""
                  title=""
                >
                  <i class="ni ni-fat-remove pt-1"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex justify-content-center mt-3">
        <pagination
          :records="totalItems"
          :per-page="perPage"
          v-model="currentPage"
          @paginate="onPageChange"
          align="center"
        ></pagination>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { backendUrl } from "../main.js";
import Pagination from "vue-pagination-2";

export default {
  components: {
    Pagination,
  },
  data() {
    return {
      booking: null,
      currentPage: 1,
      perPage: 5,
      totalItems: 0,
    };
  },
  mounted() {
    this.listBookings();
  },
  computed: {
    displayedBookings() {
      if (this.booking) {
        const startIndex = (this.currentPage - 1) * this.perPage;
        const endIndex = startIndex + this.perPage;
        return this.booking.slice(startIndex, endIndex);
      } else {
        return [];
      }
    },
  },
  methods: {
    listBookings() {
      const token = localStorage.getItem("token");
      if (token) {
        axios
          .get(`${backendUrl}bookings/`, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.booking = response.data;
            this.totalItems = response.data.length;
         
          })
          .catch((error) => {
            console.error("Error en la obtención de reservas:", error);
          });
      } else {
        console.error("No se encontró el token de autenticación.");
      }
    },
    onPageChange(page) {
      this.currentPage = page;
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
