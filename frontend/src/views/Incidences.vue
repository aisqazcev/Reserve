<template>
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
    </div>
    <div class="container pt-lg-md">
      <div class="card mb-3 text-white">
        <div class="card-body">
          <h3 class="card-title">Formulario de Incidencia</h3>
          <form @submit.prevent="sendIncidence" role="form">
            <div class="ct-example-row">
              <div class="row">
                <div class="col-sm">
                  <label for="title" style="color: black">Título</label>
                  <input v-model="formData.title" type="text" id="title" class="form-control" placeholder="Introduce el título de la incidencia">
                </div>
              </div>
              <div class="row">
                <div class="col-sm">
                  <label for="description" style="color: black">Descripción</label>
                  <textarea v-model="formData.description" id="description" class="form-control" placeholder="Introduce la descripción de la incidencia"></textarea>
                </div>
              </div>
              <div class="row">
                <div class="col-sm">
                  <label for="equipment" style="color: black">Equipamiento Afectado</label>
                  <select v-model="formData.equipment" id="equipment" class="form-control">
                    <option value="">Seleccionar equipamiento</option>
                    <option v-for="equipment in equipmentList" :key="equipment.id" :value="equipment.id">{{ equipment.name }}</option>
                  </select>
                </div>
              </div>
              <div class="row mt-3">
                <div class="col-sm d-flex flex-column align-items-center justify-content-center">
                  <button :disabled="loading" type="submit" class="btn btn-primary my-4">Enviar incidencia</button>
                  <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
                    <i class="fas fa-exclamation-triangle"></i>
                    {{ errorMessage }}
                  </div>
                </div>
              </div>
            </div>
          </form>
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
      formData: {
        title: '',
        description: '',
        equipment: ''
      },
      loading: false,
      errorMessage: '',
      equipmentList: [],
    };
  },
   mounted() {
    this.fetchEquipmentList();
  },
  methods: {
     fetchEquipmentList() {
      axios.get(`${backendUrl}equipment/`)
        .then(response => {
          this.equipmentList = response.data;
        })
        .catch(error => {
          console.error('Error al obtener la lista de equipos:', error);
        });
    },
    sendIncidence() {
        if (!this.formData.title || !this.formData.description || !this.formData.equipment) {
        this.errorMessage = 'Todos los campos son obligatorios.';
        return;
      }
      const subject = this.formData.title;
      const message = this.formData.description;
      const equipment = this.formData.equipment;
      axios.post(`${backendUrl}send_incidence/`, {
          subject: subject,
          message: message,
          equipment: equipment,
        })
        .then(response => {
          console.log('Correo electrónico enviado con éxito:', response.data);
        })
        .catch(error => {
          console.error('Error al enviar el correo electrónico:', error);
        });
    }
  }
};
</script>

<style scoped>
/* Aquí puedes agregar estilos específicos para esta plantilla si es necesario */
</style>
