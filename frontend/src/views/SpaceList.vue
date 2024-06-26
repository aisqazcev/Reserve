<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
      <span style="visibility: hidden"></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
    <div class="container mt-3">
      <h1 class="mb-4">
        <span class="icon-arrow-left" @click="goBack"></span>
        {{ building.name_complete }}
        <i class="ni ni-bold-right" style="font-size: 24px; color: #303030">
        </i>
        {{ spaceDetails.name }}
      </h1>
      <card class="mb-3">
        <div class="row">
          <div class="col-md-5">
            <img
              :src="
                spaceDetails.image
                  ? getSpaceImageUrl(spaceDetails.image)
                  : '/img/alternative.jpg'
              "
              class="img-fluid shadow-lg mb-4 rounded-square"
              alt="Imagen del espacio"
            />
          </div>
          <div class="col-md-7">
            <div class="card-body-1">
              <h3 class="card-title">Detalles del Espacio</h3>
              <div
                class="d-flex align-items-center"
                style="margin-bottom: 20px"
              >
                <i
                  class="ni ni-chart-bar-32 mr-2"
                  style="font-size: 24px; color: #be0f2e"
                >
                </i>
                Capacidad: {{ spaceDetails.capacity }}
              </div>
              <div
                class="d-flex align-items-center"
                style="margin-bottom: 20px"
              >
                <div v-if="spaceDetails && spaceDetails.features">
                  Equipamiento:
                  <equipment :equipments="spaceDetails.features"></equipment>
                </div>
              </div>
              <div
                class="d-flex align-items-center"
                style="margin-bottom: 20px"
              >
                <i
                  class="fas fa-info-circle mr-2"
                  style="font-size: 24px; color: #be0f2e"
                ></i>
                <td>{{ spaceDetails.general_info }}</td>
              </div>
            </div>
          </div>
        </div>
      </card>
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-md-4 mb-3">
              <div class="form-group">
                <label for="fecha">Fecha:</label>
                <input
                  type="date"
                  id="date"
                  v-model="reservationDate"
                  :min="minDate"  
                  class="form-control"
                />
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="form-group">
                <label for="horaInicio">Hora de inicio:</label>
                <input
                  type="time"
                  id="start_time"
                  v-model="reservationStartTime"
                  :min="minTime" 
                  class="form-control"
                />
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <div class="form-group">
                <label for="duracion">Duración:</label>
                <select
                  id="duration"
                  v-model="duration"
                  class="form-control"
                  @change="handleDurationChange"
                >
                  <option value="15">0:15</option>
                  <option value="30">0:30</option>
                  <option value="45">0:45</option>
                  <option value="60">1:00</option>
                  <option value="75">1:15</option>
                  <option value="90">1:30</option>
                  <option value="105">1:45</option>
                  <option value="120">2:00</option>
                  <option value="135">2:15</option>
                  <option value="150">2:30</option>
                  <option value="165">2:45</option>
                  <option value="180">3:00</option>
                </select>
              </div>
            </div>
            <div class="col-md-12">
              <dt>
                <div
                  v-if="showNoResultsMessage"
                  class="alert alert-default"
                  role="alert"
                >
                  No hay resultados para la búsqueda.
                </div>
                <div
                  v-if="errorMessage"
                  class="alert alert-default error-message"
                  role="alert"
                >
                  <i class="fas fa-exclamation-triangle"></i>
                  {{ errorMessage }}
                </div>
              </dt>
              <button
                class="btn btn-primary btn-block"
                @click="searchDisponibility"
              >
                Buscar Disponibilidad
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="bookingMessage" class="alert alert-success" role="alert">
        {{ bookingMessage }}
      </div>
      <div class="row mt-3" v-if="search">
        <div class="col">
          <div class="table-container">
            <table class="table">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Asientos cercanos</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in spacesItems" :key="index">
                  <td data-label="Nombre">{{ item.name }}</td>
                  <td data-label="Asientos cercanos">
                    {{ formatDeskNames(item.nearby_desks_names) }}
                  </td>
                  <td data-label="Acciones">
                    <button
                      class="btn btn-primary"
                      @click="bookingDesk(item.id)"
                    >
                      Reservar
                    </button>
                  </td>
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
import "@fortawesome/fontawesome-free/css/all.css";
import Card from "../components/Card.vue";
import Equipment from "../components/Equipment.vue";

export default {
  components: { Equipment, Card },
  data() {
    const now = new Date();
    const currentDate = now.toISOString().substring(0, 10);
    now.setMinutes(0, 0, 0);
    now.setHours(now.getHours() + 1);
    const nextHour = `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}`;

    return {
      spacesItems: [],
      spaceDetails: {},
      building: {},
      campus: {},
      originalSpacesItems: [],
      errorMessage: "",
      showModal: false,
      reservationDate: currentDate,
      reservationStartTime: nextHour,
      duration: 60,
      reservedSeat: "",
      showNoResultsMessage: false,
      userReservations: "",
      search: false,
      bookingMessage: "",
      minDate: currentDate,
      minTime: nextHour,
    };
  },
  mounted() {
    this.listSpaceItems();
    this.getSpaceDetails();

    const routeQuery = this.$route.query;

    if (routeQuery.date && routeQuery.time && routeQuery.duration) {
      this.reservationDate = routeQuery.date;
      document.getElementById("date").value = routeQuery.date;

      this.reservationStartTime = routeQuery.time;
      document.getElementById("start_time").value = routeQuery.time;

      this.duration = routeQuery.duration;
      
    }
    this.checkDate();
  },
  methods: {
    checkDate() {
      if (this.reservationDate === this.minDate) {
        const now = new Date();
        const currentHour = now.getHours().toString().padStart(2, "0");
        const currentMinute = now.getMinutes().toString().padStart(2, "0");
        this.minTime = `${currentHour}:${currentMinute}`;
      } else {
        this.minTime = "00:00";
      }
    },
    formatDeskNames(deskNames) {
      return deskNames.join(", ");
    },
    goBack() {
      this.$router.go(-1);
    },
    handleDurationChange(event) {},
    listSpaceItems() {
      const token = localStorage.getItem("token");
      const spaceId = this.$route.params.spaceId;
      if (token) {
        axios
          .get(`${backendUrl}bookings/`, {
            headers: { Authorization: `Token ${token}` },
       
        })
          .then((response) => {
            this.userReservations = response.data;
        })
          .catch((error) => {
            console.error("Error al obtener reservas del usuario:", error);
          });
        axios
          .get(`${backendUrl}${spaceId}/desk/`, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.spacesItems = response.data;
            this.originalSpacesItems = response.data;
          })
          .catch((error) => {
            console.error("Error en la obtención de items de espacio:", error);
          });
      } else {
        console.error("No se encontró el token de autenticación.");
      }
    },
    getSpaceDetails() {
      const token = localStorage.getItem("token");
      const spaceId = this.$route.params.spaceId;
      if (token) {
        axios
          .get(`${backendUrl}space/${spaceId}/`, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.spaceDetails = response.data;
            this.spaceDetails.features = response.data.features;

            const buildingId = response.data.building;
            axios
              .get(`${backendUrl}building/${buildingId}/`)
              .then((buildingResponse) => {
                this.building = buildingResponse.data;
              })
              .catch((error) => {
                console.error(
                  "Error al obtener los detalles del edificio:",
                  error
                );
              });
          })
          .catch((error) => {
            console.error("Error al obtener los detalles del espacio:", error);
          });
      } else {
        console.error("No se encontró el token de autenticación.");
      }
    },

    isPastDate(dateString) {
      const selectedDate = new Date(dateString);
      const currentDate = new Date();
      currentDate.setHours(0, 0, 0, 0);
      return selectedDate < currentDate;
    },

    isPastTime(timeString) {
      const currentTime = new Date();
      const [hours, minutes] = timeString.split(":");
      const selectedTime = new Date();
      selectedTime.setHours(hours, minutes, 0, 0);

      return selectedTime < currentTime;
    },

    searchDisponibility() {
    
    this.errorMessage = "";
    const date = document.getElementById("date").value;
    const start_time = document.getElementById("start_time").value;
    const duration = document.getElementById("duration").value;
    const spaceId = this.$route.params.spaceId;

    if (this.isPastDate(date)) {
      this.search = false;
      this.errorMessage = "No se puede seleccionar una fecha pasada.";
      return;
    }

    if (date === this.getCurrentDate() && this.isPastTime(start_time)) {
      this.search = false;
      this.errorMessage =
        "No se puede seleccionar una hora anterior a la hora actual para el día de hoy.";
      return;
    }
    this.search = true;
    const startDateTime = new Date(`${date}T${start_time}`);
    const startDateTimeUTC = new Date(startDateTime.getTime() - (startDateTime.getTimezoneOffset() * 60000)).toISOString().slice(0, 16);

    axios
      .get(`${backendUrl}find-available-seats/`, {
        params: {
          start_time: startDateTimeUTC,
          duration: duration,
          space_id: spaceId,
        },
      })
      .then((response) => {
        const availableSeats = response.data.available_seats;
        const filteredSeats = this.originalSpacesItems.filter((seat) =>
          availableSeats.includes(seat.id)
        );

        this.spacesItems = filteredSeats.map((seat) => ({
          ...seat,
          seat_status: "AVAILABLE",
        }));
        if (this.spacesItems.length === 0) {
          this.showNoResultsMessage = true;
        } else {
          this.showNoResultsMessage = false;
        }
      })
      .catch((error) => {
        console.error("Error al buscar disponibilidad:", error);
      });
  },
  bookingDesk(deskId) {
    const date = document.getElementById("date").value;
    const startTimeInput = document.getElementById("start_time").value;
    const durationMinutes = parseInt(document.getElementById("duration").value);
    const spaceId = this.$route.params.spaceId;

    const startDate = new Date(`${date}T${startTimeInput}`);
    const startDateUTC = new Date(startDate.getTime() - (startDate.getTimezoneOffset() * 60000)).toISOString().slice(0, 16);
    const endDate = new Date(startDate.getTime() + durationMinutes * 60000);
    const endDateUTC = new Date(endDate.getTime() - (endDate.getTimezoneOffset() * 60000)).toISOString().slice(0, 16);

    let overlappingReservation = this.userReservations.some((reservation) => {
        const reservationStartDate = new Date(reservation.start_time).toISOString().slice(0, 16);
        const reservationEndDate = new Date(reservation.end_time).toISOString().slice(0, 16);

        if (reservationStartDate.toString === startDateUTC.toString) {
            return (
                startDateUTC < reservationEndDate && endDateUTC > reservationStartDate
            );
        }
        return false;
    });

    if (overlappingReservation) {
        this.errorMessage =
            "Ya tienes una reserva en esta franja horaria para el mismo día.";
        return;
    }

    const token = localStorage.getItem("token");
    if (token) {
        axios
            .post(
                `${backendUrl}booking/`,
                {
                    desk: deskId,
                    date: date,
                    start_time: startDateUTC,
                    duration: durationMinutes,
                    end_time: endDateUTC,
                    space_id: spaceId,
                },
                {
                    headers: { Authorization: `Token ${token}` },
                }
            )
            .then((response) => {
                this.spacesItems = this.spacesItems.filter(
                    (item) => item.id !== deskId
                );
                this.bookingMessage = "Reserva exitosa. Correo enviado con los detalles.";
                setTimeout(() => window.location.reload(), 1500);
            })
            .catch((error) => {
                this.errorMessage =
                    "Error al reservar el escritorio: " + error.message;
            });
    } else {
        this.errorMessage = "No se encontró el token de autenticación.";
    }
}
,

  getCurrentDate() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, "0");
    const day = String(currentDate.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  },
    getSpaceImageUrl(relativePath) {
      relativePath = relativePath.replace(/^\/media*/, "");
      const imageUrl = `${backendUrl}${relativePath}`;
      return imageUrl;
    },
  },
};
</script>

<style>
.card {
  background-color: rgba(159, 216, 197, 0.5);
}

.table-container {
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  overflow: hidden;
}

.table-container table {
  background-color: transparent;
}

.rounded-square {
  border-radius: 5px;
}

.icon-arrow-left {
  color: #be0f2e;
}

.icon-arrow-left:hover {
  color: #0f1af2;
}
</style>