<template>
  <div class="relative bg-gray-50 pt-16 pb-20 px-4 sm:px-6 lg:pt-24 lg:pb-28 lg:px-8">
    <div class="absolute inset-0">
      <div class="bg-white h-1/3 sm:h-2/3" />
    </div>
    <div class="relative max-w-7xl mx-auto">
      <div class="text-center">
        <h1> holi</h1>
      </div>

      <div class="mt-12 max-w-lg mx-auto grid gap-5 lg:grid-cols-3 lg:max-w-none">
        <li v-for="equipment in APIData" :key="equipment.id">
        <router-link :to="'/equipment/' + equipment.id">{{ equipment.name }}</router-link>
        <p>{{ equipment.institution }}</p>
      </li>
      </div>
    </div>

  </div>
</template>


<script>
import { getAPI } from '../axios-api'

export default {
  name: 'EquipmentAdmin',
  data () {
    return {
      APIData: []
    }
  },
  created () {
        getAPI.get('/reserve/equipment/',) //Aqui va la ruta del backend con la que se obtiene los datos
          .then(response => {
            console.log('Post API has recieved data')
            this.APIData = response.data
          })
          .catch(err => {
            console.log(err)
          })
    }
}
</script>