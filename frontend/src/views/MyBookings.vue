<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container mt-0 mb-3">
      <h1 class="mb-4" style="color: #051551">Reservas</h1>
      <div class="mb-3">
        <button
          @click="filterPastBookings"
          :class="{
            'btn-primary': selectedOption === 'past',
            'btn-secondary': selectedOption !== 'past',
          }"
          class="btn mr-2"
          style="text-transform: none"
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
          style="text-transform: none"
        >
          Próximas
        </button>
      </div>
      <div v-if="bookingMessage" class="alert alert-success alert-dismissible" role="alert">
        {{ bookingMessage }}
        <button type="button" class="close" @click="closeBookingMessage" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div v-if="bookingError" class="alert alert-default alert-dismissible" role="alert">
        {{ bookingError }}
        <button type="button" class="close" @click="closeBookingError" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
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
              <th v-if="selectedOption === 'future'">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in displayedBookings" :key="index">
              <td data-label="Fecha">{{ formatDate(item.date) }}</td>
              <td data-label="Hora inicio">
                {{ formatHour(item.start_time) }}
              </td>
              <td data-label="Hora fin">{{ formatHour(item.end_time) }}</td>
              <td data-label="Asiento">{{ item.deskName }}</td>
              <td data-label="Sala">{{ item.spaceName }}</td>
              <td data-label="Edificio">{{ item.name_complete }}</td>
              <td class="td-actions" v-if="isFutureBooking(item)">
                <button
                  type="button"
                  rel="tooltip"
                  class="btn btn-default btn-icon btn-sm"
                  @click="openInviteModal(item)"
                >
                  <i class="ni ni-circle-08 pt-1"></i>
                </button>
                <modal
                  v-if="showInviteModal"
                  :show.sync="showInviteModal"
                  body-classes="p-0"
                  modal-classes="modal-dialog-centered modal-sm"
                >
                  <card
                    type="secondary"
                    shadow
                    header-classes="bg-white pb-5"
                    body-classes="px-lg-5 py-lg-5"
                    class="border-0"
                  >
                    <template>
                      <div class="text-center text-muted mb-4">
                        <h2>¿A quién quieres invitar?</h2>
                      </div>
                      <form @keydown.enter.prevent @submit.prevent="invite">
                        <base-input
                          alternative
                          class="mb-3"
                          placeholder="Email del usuario invitado"
                          v-model="invitedEmail"
                          type="email"
                        ></base-input>
                        <div
                          v-if="inviteError"
                          class="alert alert-default alert-dismissible"
                          role="alert"
                        >
                          {{ inviteError }}
                          <button type="button" class="close" @click="closeInviteError" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                          </button>
                        </div>
                        <div class="text-center">
                          <base-button
                            type="primary"
                            class="my-4"
                            @click="search_available_nearby(selectedBooking)"
                            >Invitar</base-button
                          >
                        </div>
                      </form>
                    </template>
                  </card>
                </modal>
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
      selectedOption: "future",
      filteredBookings: [],
      bookingError: "",
      inviteError: "",
      bookingMessage: "",
      showInviteModal: false,
      invitedEmail: "",
      selectedBooking: null,
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
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.filteredBookings.slice(startIndex, endIndex);
    },
  },
  methods: {
    isFutureBooking(item) {
      const endDateTime = new Date(item.end_time);
      const currentDate = new Date();
      return endDateTime > currentDate;
    },
    closeErrorMessage() {
      this.bookingError = "";
      this.inviteError = "";
    },
    closeBookingMessage() {
      this.bookingMessage = "";
    },
    closeBookingError() {
      this.bookingError = "";
    },
    closeInviteError() {
      this.inviteError = "";
    },

    filterPastBookings() {
      this.selectedOption = "past";
      const currentDate = new Date();

      this.currentPage = 1;
      if (this.booking !== null) {
        this.filteredBookings = this.booking.filter((booking) => {
          const endDateTime = new Date(booking.end_time);
          return endDateTime < currentDate;
        });
        this.totalItems = this.filteredBookings.length;
      }
    },
    filterFutureBookings() {
      this.selectedOption = "future";
      const currentDate = new Date();

      this.currentPage = 1;
      if (this.booking !== null) {
        this.filteredBookings = this.booking.filter((booking) => {
          const endDateTime = new Date(booking.end_time);
          return endDateTime > currentDate;
        });
        this.totalItems = this.filteredBookings.length;
      }
    },
    toggleSortDirection() {
      this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
      this.sortBookingsByDate(this.filteredBookings);
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
        spacePromises.push(axios.get(`${backendUrl}space/${booking.space}/`));
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
            booking.name_complete = responses[buildingIndex].data.name_complete;
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
    formatDate(date) {
      const dateObject = new Date(date);
      return dateObject.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        timeZone: "UTC",
      });
    },
    formatHour(dateTime) {
      const date = new Date(dateTime);
      return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        timeZone: "UTC",
      });
    },
    cancelBooking(bookingId, index) {
      const bookingToCancel = this.displayedBookings[index];

      if (bookingToCancel) {
        const startDateTime = new Date(bookingToCancel.start_time);
        const currentDateTime = new Date();
        const timeDifference =
          startDateTime.getTime() - currentDateTime.getTime();
        const hoursDifference = timeDifference / (1000 * 60 * 60);

        if (hoursDifference <= 4) {
          this.bookingError =
            "No se pueden cancelar reservas que comienzan en 4 horas o menos.";
          setTimeout(() => {
            this.bookingError = "";
          }, 5000);
          return;
        }
      }
      const token = localStorage.getItem("token");
      axios
        .delete(`${backendUrl}booking/${bookingId}/`, {
          headers: { Authorization: `Token ${token}` },
        })
        .then((response) => {
          this.displayedBookings.splice(index, 1);
          this.totalItems--;
          this.totalItems = this.filteredBookings.length;
          this.listBookings().then(() => {
            this.sortBookingsByDate();
            this.filterFutureBookings();
          });
          this.bookingMessage = "Reserva cancelada con éxito.";
          setTimeout(() => {
            this.bookingMessage = "";
          }, 5000);
        })
        .catch((error) => {
          console.error("Error al cancelar la reserva:", error);
          if (error.response && error.response.data && error.response.data.error) {
            this.bookingError = error.response.data.error;
          } else {
            this.bookingError = "Ocurrió un error al cancelar la reserva.";
          }
          setTimeout(() => {
            this.bookingError = "";
          }, 5000);
        });
    },
    openInviteModal(booking) {
      this.selectedBooking = booking;
      this.showInviteModal = true;
      this.inviteError = ""; // Limpiar el mensaje de error cuando se abre el modal
    },
    closeInviteModal() {
      this.showInviteModal = false;
      this.selectedBooking = null;
    },
    search_available_nearby(booking) {
      axios
        .post(`${backendUrl}find_nearby_seats/`, {
          desk_id: booking.desk,
        })
        .then((nearbyResponse) => {
          if (nearbyResponse.data.nearby_seat_ids.length > 0) {
            const formattedStartTime = new Date(booking.start_time)
              .toISOString()
              .slice(0, 16);
            const durationInMinutes = parseInt(booking.duration);
            axios
              .get(`${backendUrl}find-available-seats/`, {
                params: {
                  start_time: formattedStartTime,
                  duration: durationInMinutes,
                  desk_id: booking.desk,
                  space_id: booking.space,
                },
              })
              .then((availableResponse) => {
                if (availableResponse.data.available_seats.length > 0) {
                  const availableSeatIds = nearbyResponse.data.nearby_seat_ids;
                  const nearbySeatsIds = nearbyResponse.data.nearby_seat_ids;
                  let nearbySeatAvailable = false;
                  for (const availableSeat of availableSeatIds) {
                    if (nearbySeatsIds.includes(availableSeat)) {
                      nearbySeatAvailable = true;
                      this.invite(booking, availableSeatIds);
                      break;
                    }
                  }
                }
              });
          }
        })
        .catch((error) => {
          console.error("Error al buscar asientos cercanos:", error);
          this.inviteError = "Ocurrió un error al buscar asientos cercanos.";
          setTimeout(() => {
            this.inviteError = "";
          }, 5000);
        });
    },
    invite(booking, nearbySeats) {
      const token = localStorage.getItem("token");
      if (token) {
        axios
          .get(`${backendUrl}profile/`, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.userData = response.data;
            axios
              .post(`${backendUrl}invite/`, {
                invited_email: this.invitedEmail,
                user_data: this.userData,
                booking_data: booking,
                nearby_seats: nearbySeats,
              })
              .then((response) => {
                this.showInviteModal = false;
                this.invitedEmail = "";
                this.bookingMessage = "Correo de invitación enviado con éxito.";
                setTimeout(() => {
                  this.bookingMessage = "";
                }, 5000);
              })
              .catch((error) => {
                console.error("Error al invitar:", error);
                // Obtener el mensaje de error específico del backend
                if (error.response && error.response.data && error.response.data.error) {
                  this.inviteError = error.response.data.error;
                } else {
                  this.inviteError = "Ocurrió un error al enviar la invitación.";
                }
                setTimeout(() => {
                  this.inviteError = "";
                }, 5000);
              });
          })
          .catch((error) => {
            console.error("Error al obtener los datos:", error);
            if (error.response && error.response.data && error.response.data.error) {
              this.inviteError = error.response.data.error;
            } else {
              this.inviteError = "Ocurrió un error al obtener los datos del usuario.";
            }
            setTimeout(() => {
              this.inviteError = "";
            }, 5000);
          });
      } else {
        console.error("No se encontró el token de autenticación.");
        this.inviteError = "No se encontró el token de autenticación.";
        setTimeout(() => {
          this.inviteError = "";
        }, 5000);
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
