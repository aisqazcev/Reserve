<template>
    <section class="section section-shaped section-lg my-0">
      <div class="shape shape-style-1 bg-gradient-default">
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
        <div class="row justify-content-center">
          <div class="col-lg-5">
            <card
              type="secondary"
              shadow
              header-classes="bg-white pb-5"
              body-classes="px-lg-5 py-lg-5"
              class="border-0"
            >
              <template>
                <div class="text-center mb-3">
                  <small>Crea tu usuario</small>
                </div>
                <form @submit.prevent="register" role="form">
                  <base-input
                    alternative
                    class="mb-3"
                    placeholder="Usuario"
                    v-model="form.username"
                    addon-left-icon="ni ni-hat-3"
                  ></base-input>
                  <base-input
                    alternative
                    class="mb-3"
                    placeholder="Nombre"
                    v-model="form.name"
                    addon-left-icon="ni ni-single-02"
                  ></base-input>
                  <base-input
                    alternative
                    class="mb-3"
                    placeholder="Email"
                    v-model="form.email"
                    addon-left-icon="ni ni-email-83"
                  ></base-input>
                  <base-input
                    alternative
                    type="password"
                    placeholder="Contraseña"
                    v-model="form.password"
                    addon-left-icon="ni ni-lock-circle-open"
                  ></base-input>
                  <base-input
                    alternative
                    type="password"
                    placeholder="Confirmar Contraseña"
                    v-model="form.password2"
                    addon-left-icon="ni ni-lock-circle-open"
                  ></base-input>
                  <div class="text-center">
                    <base-button
                      :disabled="loading"
                      type="primary"
                      class="my-4"
                      @click="register"
                    >
                      Crear Usuario
                    </base-button>
                  </div>
                </form>
              </template>
            </card>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  import axios from 'axios'
  import { backendUrl } from "../main.js";
  
  
  export default {
    name: 'SignUp', 
    data(){
      return{
        form: {
          username: '',
          password: '',
          password2: '',
          name: '', 
          email: '',
        },
        errors: [],
        loading: false,
      }
    },
    methods:{
      async register(){
        this.errors = []
        this.loading = true;
  
        if(this.form.username === ''){
          this.errors.push('The username is missing')
        }
        if(this.form.password === '' || this.form.password2 === ''){
          this.errors.push('The password is missing')
        }
        if(this.form.password2 !== this.form.password){
          this.errors.push('The passwords don\'t match')
        }
        if(!this.errors.length){
          try {
            const response = await axios.post(`${backendUrl}register/`, this.form);
            
            this.loading = true;
            setTimeout(() => {
              this.$router.push("/");
              this.loading = false;
            }, 2000);
          } catch (error) {
            this.errors.register = "Ha ocurrido un error. Por favor, inténtelo de nuevo.";
            console.error("Register error:", error);
          }
        }
      }
    }
  }
  </script>