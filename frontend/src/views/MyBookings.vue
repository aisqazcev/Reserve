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
              <th>
                Fecha
                <i
                  class="fas fa-sort ml-2"
                  :class="
                    sortDirection === 'asc' ? 'fa-sort-up' : 'fa-sort-down'
                  "
                  @click="toggleSortDirection"
                ></i>
              </th>

              <th>Hora inicio</th>
              <th>Hora fin</th>
              <th>Asiento</th>
              <th>Sala</th>
              <th>Edificio</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in displayedBookings" :key="index">
              <td data-label="Fecha">{{ item.date }}</td>
              <td data-label="Hora inicio">
                {{ formatHour(item.start_time) }}
              </td>
              <td data-label="Hora fin">{{ formatHour(item.end_time) }}</td>
              <td data-label="Asiento">{{ item.deskName }}</td>
              <td data-label="Sala">{{ item.spaceName }}</td>
              <td data-label="Edificio">{{ item.buildingName }}</td>
              <td class="td-actions">
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
      isLoading: true,
      sortDirection: "desc",
    };
  },
  mounted() {
    this.listBookings();
    this.sortBookingsByDate();
  },
  computed: {
    displayedBookings() {
      if (!this.booking) return [];
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.booking.slice(startIndex, endIndex);
    },
  },
  methods: {
    toggleSortDirection() {
      this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
      this.sortBookingsByDate();
    },
    sortBookingsByDate() {
      if (this.booking) {
        this.booking.sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);

          const directionFactor = this.sortDirection === "asc" ? 1 : -1; 
          
          if (dateA > dateB) return -1 * directionFactor;
          if (dateA < dateB) return 1 * directionFactor;

          const timeA = new Date(a.start_time);
          const timeB = new Date(b.start_time);
          return (timeA - timeB) * directionFactor;
        });
      }
    },
    async listBookings() {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("No se encontró el token de autenticación.");
        return;
      }
      try {
        const response = await axios.get(`${backendUrl}bookings/`, {
          headers: { Authorization: `Token ${token}` },
        });
        this.booking = response.data;
        this.totalItems = this.booking.length;
        await this.getBookingDetails();
      } catch (error) {
        console.error("Error en la obtención de reservas:", error);
      }
    },
    getBookingDetails() {
      const deskPromises = [];
      const spacePromises = [];
      const buildingPromises = [];

      this.booking.forEach((booking) => {
        deskPromises.push(axios.get(`${backendUrl}desk/${booking.desk}/`));
        spacePromises.push(axios.get(`${backendUrl}spaces/${booking.space}/`));
        buildingPromises.push(
          axios.get(`${backendUrl}building/${booking.building}/`)
        );
      });

      Promise.all([...deskPromises, ...spacePromises, ...buildingPromises])
        .then((responses) => {
          this.booking.forEach((booking, index) => {
            const deskIndex = index;
            const spaceIndex = index + this.booking.length;
            const buildingIndex = index + this.booking.length * 2;
            booking.deskName = responses[deskIndex].data.name;
            booking.spaceName = responses[spaceIndex].data.name;
            booking.buildingName = responses[buildingIndex].data.name;
          });

          this.isLoading = false;

          this.$forceUpdate();
        })
        .catch((error) => {
          console.error("Error obteniendo detalles:", error);
          this.isLoading = false;
        });
    },
    onPageChange(page) {
      this.currentPage = page;
    },
    formatHour(dateTime) {
      const date = new Date(dateTime);
      return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
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
  width: 100%;
}
.table td {
  text-align: center;
}
.table thead th {
  text-align: center;
}
.table tbody tr:nth-child(odd) {
  background-color: #f2f2f2;
}

@media only screen and (max-width: 600px) {
  .table thead {
    display: none;
  }
  .table td {
    display: block;
    width: 100%;
    text-align: left;
    padding: 10px;
  }
  .table td::before {
    content: attr(data-label);
    font-weight: bold;
    float: left;
    text-transform: capitalize;
    padding-right: 5px;
  }
}
</style>
