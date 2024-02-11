<template>
  <section class="section-shaped section-lg my-0 d-flex justify-content-center">
    <div class="shape shape-style-3 shape-default">
      <span style="visibility: hidden;"></span>
      <span></span>
      <span></span>
      <span style="background-color: #787CFF;"></span>
    </div>
    <div class="container mt-3">
      <h2 class="card-title">{{ spaceDetails.name }} de {{ building.name }}</h2>
      <div class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">Detalles del Espacio</h5>
          <p><strong>Nombre:</strong> {{ spaceDetails.name }}</p>
          <p><strong>Ubicación:</strong> {{ spaceDetails.location }}</p>
        </div>
      </div>
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
                <label for="duracion">Duración:</label>
                <select
                  id="duration"
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
                  class="alert alert-info"
                  role="alert"
                >
                  No hay resultados para la búsqueda.
                </div>
                <div
                  v-if="errorMessage"
                  class="alert alert-warning error-message"
                  role="alert"
                >
                  <i class="fas fa-exclamation-triangle"></i>
                  {{ errorMessage }}
                </div>
              </dt>
              <button
                class="btn btn-primary btn-block"
                @click="buscarDisponibilidad"
              >
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
                  <td>
                    <button
                      class="btn btn-primary"
                      @click="reservarDesk(item.id)"
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
      <!-- Modal para mostrar la reserva exitosa -->
<div class="modal" :class="{ 'show': showModal }">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Reserva Exitosa</h5>
        <button type="button" class="close" @click="closeModal">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>Fecha: {{ reservationDate }}</p>
        <p>Hora de inicio: {{ reservationStartTime }}</p>
        <p>Asiento: {{ reservedSeat }}</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="closeModal">Cerrar</button>
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
import "@fortawesome/fontawesome-free/css/all.css";


export default {
  data() {
    return {
      spacesItems: [],
      spaceDetails: {},
      building: {},
      campus: {},
      originalSpacesItems: [],
      errorMessage: "",
      showModal: false,
      reservationDate: "",
      reservationStartTime: "",
      reservedSeat: "",
    };
  },
  mounted() {
    this.listSpaceItems();
    this.getSpaceDetails();
  },
  methods: {
    openModal() {
    this.showModal = true;
  },
  closeModal() {
    this.showModal = false;
  },
    handleDurationChange(event) {
      console.log("Duración seleccionada:", event.target.value);
    },
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
            this.originalSpacesItems = response.data;
            console.log("datos: ", response.data);
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
          .get(`${backendUrl}spaces/${spaceId}/`, {
            headers: { Authorization: `Token ${token}` },
          })
          .then((response) => {
            this.spaceDetails = response.data;
            console.log("Detalles del espacio: ", response.data);

            const buildingId = response.data.building;
            axios
              .get(`${backendUrl}building/${buildingId}/`)
              .then((buildingResponse) => {
                this.building = buildingResponse.data;
                console.log("Detalles del edificio: ", buildingResponse.data);
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
      currentDate.setHours(0, 0, 0, 0); // Ajustar la fecha actual a medianoche

      return selectedDate < currentDate;
    },

    // Método para verificar si una hora es anterior a la hora actual
    isPastTime(timeString) {
      const currentTime = new Date();
      const [hours, minutes] = timeString.split(":");
      const selectedTime = new Date();
      selectedTime.setHours(hours, minutes, 0, 0);

      return selectedTime < currentTime;
    },

    buscarDisponibilidad() {
      const date = document.getElementById("date").value;
      const start_time = document.getElementById("start_time").value;
      const duration = document.getElementById("duration").value;
      const spaceId = this.$route.params.spaceId; // Obtener el ID de la sala actual

      console.log("Fecha:", date);
      console.log("Hora de inicio:", start_time);
      console.log("Duración:", duration);
      console.log("ID de la sala:", spaceId);

      if (this.isPastDate(date)) {
        this.errorMessage = "No se puede seleccionar una fecha pasada.";
        return;
      }

      if (date === this.getCurrentDate() && this.isPastTime(start_time)) {
        this.errorMessage =
          "No se puede seleccionar una hora anterior a la hora actual para el día de hoy.";
        return;
      }

      axios
        .get(`${backendUrl}find-available-seats/`, {
          params: {
            start_time: `${date} ${start_time}`,
            duration: duration,
            space_id: spaceId,
            date: date,
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
            this.showNoResultsMessage = true; // Activar la bandera para mostrar el mensaje de no resultados
          } else {
            this.showNoResultsMessage = false; // Desactivar la bandera si hay resultados
          }
        })
        .catch((error) => {
          console.error("Error al buscar disponibilidad:", error);
        });
    },
    getCurrentDate() {
      const currentDate = new Date();
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, "0");
      const day = String(currentDate.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    },

    reservarDesk(deskId) {
      const date = document.getElementById("date").value;
      const start_time = document.getElementById("start_time").value;
      const durationMinutes = parseInt(
        document.getElementById("duration").value
      ); // Duración en minutos
      const spaceId = this.$route.params.spaceId; // Obtener el ID de la sala actual

      const startTimeSplit = start_time.split(":");
      const startHour = parseInt(startTimeSplit[0]);
      const startMinute = parseInt(startTimeSplit[1]);
      const endMinute = startMinute + durationMinutes;
      const endHour = startHour + Math.floor(endMinute / 60);
      const endMinuteAdjusted = endMinute % 60;

      // Convertir duración de minutos a horas y minutos
      const durationHours = Math.floor(durationMinutes / 60);
      const durationMinutesRemainder = durationMinutes % 60;

      // Formatear la duración como hh:mm:ss
      const formattedDuration = `${durationHours
        .toString()
        .padStart(2, "0")}:${durationMinutesRemainder
        .toString()
        .padStart(2, "0")}:00`;

      const end_time =
        new Date(`${date} ${start_time}`).getTime() +
        durationMinutes * 60 * 1000;
      const formattedEndTime = new Date(end_time)
        .toISOString()
        .slice(0, 19)
        .replace("T", " ");

      const token = localStorage.getItem("token");
      if (token) {
        axios
          .post(
            `${backendUrl}booking/`,
            {
              desk: deskId,
              date: date,
              start_time: `${date} ${start_time}`,
              duration: formattedDuration, 
              end_time: formattedEndTime,
              space_id: spaceId,
            },
            {
              headers: { Authorization: `Token ${token}` },
            }
          )
          .then((response) => {
            console.log("Reserva exitosa:", response.data);
            
            this.reservationDate = date;
        this.reservationStartTime = start_time;
        this.reservedSeat = deskId;
        this.$nextTick(() => { // Espera hasta que se hayan aplicado los cambios en el DOM
          this.openModal(); // Abre el modal después de que Vue.js haya actualizado la vista
        });
        this.spacesItems = this.spacesItems.filter(
          (item) => item.id !== deskId
        );
      })
          .catch((error) => {
            this.errorMessage = "Error al reservar el escritorio.";
          });
      } else {
        this.errorMessage = "No se encontró el token de autenticación.";
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
