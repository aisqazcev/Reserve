<template>
  <div class="equipment">
    <span
      v-for="(equipment, index) in mappedEquipments"
      :key="index"
      class="equipment-item"
    >
      <i
        :class="getIconClass(equipment)"
        @mouseover="showEquipmentName(index)"
        @mouseleave="hideEquipmentName(index)"
      ></i>
      <span class="equipment-name" :class="{ 'visible': showEquipmentNames && isHovered[index] }">
        {{ equipment }}
      </span>
    </span>
  </div>
</template>

<script>
export default {
  props: {
    equipments: {
      type: Array,
      required: true,
    },
    showEquipmentNames: {
      type: Boolean,
      default: true, // Por defecto, mostrar los nombres de los equipos
    },
  },
  data() {
    return {
      mappedEquipments: [],
      isHovered: [],
    };
  },
  mounted() {
    this.mapEquipments();
  },
  methods: {
    mapEquipments() {
      this.mappedEquipments = this.equipments.map(this.mapEquipmentToIcon);
      this.isHovered = Array(this.mappedEquipments.length).fill(false);
    },
    mapEquipmentToIcon(equipmentNumber) {
      switch (equipmentNumber) {
        case 1:
          return 'WHEELCHAIR';
        case 2:
          return 'WIFI';
        case 3:
          return 'POWER_PLUG';
        case 4:
          return 'BYCICLE';
        case 5:
          return 'LOCKER';
        case 6:
          return 'CAFETERIA';
        case 7:
          return 'PRINTER';
        case 8:
          return 'VENDING_MACHINE';
        case 9:
          return 'AIR_CONDITIONING';

        default:
          return 'UNKNOWN';
      }
    },
    getIconClass(equipmentName) {
      switch (equipmentName) {
        case 'WHEELCHAIR':
          return 'icon-wheelchair';
        case 'WIFI':
          return 'icon-connection';
        case 'POWER_PLUG':
          return 'icon-power-cord';
        case 'BYCICLE':
          return 'icon-bicycle';
        case 'LOCKER':
          return 'icon-lock';
        case 'CAFETERIA':
          return 'icon-cafe';
        case 'PRINTER':
          return 'icon-print';
        case 'VENDING_MACHINE':
          return 'icon-snacks';
        case 'AIR_CONDITIONING':
          return 'icon-snow';

        default:
          return 'fas fa-question'; 
      }
    },
    // Methods to handle hover effect
    showEquipmentName(index) {
      this.$set(this.isHovered, index, true); 
    },
    hideEquipmentName(index) {
      this.$set(this.isHovered, index, false);
    },
  },
};
</script>

<style>
.equipment {
  display: flex;
  flex-wrap: wrap;
  font-size: 110%;
  color: #aaaaaa;
}

.equipment-item {
  margin-right: 10px;
  margin-bottom: 5px;
}

.equipment-item i {
  margin-right: 5px;
}

.equipment-name {
  display: none; 
  margin-left: 5px; 
}

.equipment-name.visible {
  display: inline; 
}
</style>
