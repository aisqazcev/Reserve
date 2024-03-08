<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container mt-0 mb-3">
      <h1 class="mb-4" style="color: #051551;">
        Reservas
      </h1>
      <div class="mb-3">
        <button
          @click="filterPastBookings"
          :class="{
            'btn-primary': selectedOption === 'past',
            'btn-secondary': selectedOption !== 'past',
          }"
          class="btn mr-2"
          style="text-transform: none;"
        >
          Pasadas
        </button>
        <button
          @click="filterFutureBookings"
          :class="{
            'btn-primary': selectedOption === 'future',
            'btn-secondary': selectedOption !== 'future',
          }"
          class="btn"
          style="text-transform: none;"
        >
          Próximas
        </button>
      </div>
      <div
        v-if="errorMessage"
        class="alert alert-warning error-message"
        role="alert"
      >
        <i class="fas fa-exclamation-triangle"></i>
        {{ errorMessage }}
      </div>
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
              <th v-if="isFutureBookingsSelected">Acciones</th>
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
              <td class="td-actions" v-if="isFutureBookingsSelected">
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
                  class="btn btn-danger btn-icon btn-sm"
                  @click="cancelBooking(item.id, index)"
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
      displayedBookings: [],
      selectedOption: "future",
      isPastBookingsSelected: false,
      isFutureBookingsSelected: true,
      errorMessage: "",
    };
  },
  mounted() {
    this.listBookings().then(() => {
      this.sortBookingsByDate();
      this.filterFutureBookings();
    });
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
    filterPastBookings() {
      this.selectedOption = "past";
      const currentDate = new Date();

      this.displayedBookings = this.booking.filter((booking) => {
        const endDateTime = new Date(booking.end_time);
        return endDateTime < currentDate;
      });
      this.isPastBookingsSelected = true;
      this.isFutureBookingsSelected = false;
    },

    filterFutureBookings() {
      this.selectedOption = "future";
      if (this.booking !== null) {
        const currentDate = new Date();

        this.displayedBookings = this.booking.filter((booking) => {
          const endDateTime = new Date(booking.end_time);
          return endDateTime > currentDate;
        });
        this.isPastBookingsSelected = false;
        this.isFutureBookingsSelected = true;
      }
    },
    toggleSortDirection() {
      this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
      this.sortBookingsByDate(this.displayedBookings);
    },
    sortBookingsByDate(bookings) {
      if (bookings) {
        bookings.sort((a, b) => {
          const dateA = a.date;
          const dateB = b.date;

          const timeA = a.start_time;
          const timeB = b.start_time;

          let result = dateA.localeCompare(dateB);
          if (result === 0) {
            result = timeA.localeCompare(timeB);
          }
          return this.sortDirection === "asc" ? result : -result;
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
    cancelBooking(bookingId, index) {
      const bookingToCancel = this.booking.find(
        (booking) => booking.id === bookingId
      );

      if (bookingToCancel) {
        const startDateTime = new Date(bookingToCancel.start_time);
        const currentDateTime = new Date();
        const timeDifference =
          startDateTime.getTime() - currentDateTime.getTime();
        const hoursDifference = timeDifference / (1000 * 60 * 60);

        if (hoursDifference <= 4) {
          this.errorMessage =
            "No se pueden cancelar reservas que comienzan en 4 horas o menos.";
          return;
        }
      }
      const token = localStorage.getItem("token");
      axios
        .delete(`${backendUrl}booking/${bookingId}/`, {
          headers: { Authorization: `Token ${token}` },
        })
        .then((response) => {
          this.booking = this.booking.filter(
            (booking) => booking.id !== bookingId
          );
          this.displayedBookings.splice(index, 1);
        })
        .catch((error) => {
          console.error("Cancellation Error:", error);
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
