<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="username">Usuario:</label>
        <input type="text" id="username" v-model="form.username" />
        <span class="text-danger">{{ errors.username }}</span>
      </div>
      <div>
        <label for="password">Contraseña:</label>
        <input type="password" id="password" v-model="form.password" />
        <span class="text-danger">{{ errors.password }}</span>
      </div>
      <div>
        <label>
          <input type="checkbox" v-model="form.remember" />
          Recordarme
        </label>
      </div>
      <div>
        <button :disabled="loading" type="submit">
          Iniciar
        </button>
      </div>
      <span class="text-danger">{{ errors.login }}</span>
    </form>
  </div>
</template>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import { backendUrl } from "../main.js";

export default {
  name: "Login",
  data() {
    return {
      form: {
        username: "",
        password: "",
        remember: false,
      },
      loading: false,
      errors: {
        username: "",
        password: "",
        login: "",
      },
    };
  },
  methods: {
    async handleSubmit() {
      console.log("handleSubmit called");
      const response = await axios.post(`${backendUrl}login/`, this.form);
   
      console.log("response", response.status);
      // Mocking a login request, adjust as needed
      this.loading = true;
      setTimeout(() => {
        // Assuming a successful login, redirect to profile
        this.$router.push("/profile");
        this.loading = false;
      }, 2000);
    },
  },
};
</script>

<style>
/* Add custom styles if necessary */
</style>