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
      <span class="equipment-name" :class="{ 'visible': isHovered[index] }">
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
          return 'fas fa fa-wheelchair-alt';
        case 'WIFI':
          return 'fas fa-wifi';
        case 'POWER_PLUG':
          return 'fas fa-plug';
        case 'BYCICLE':
          return 'fas fa-bicycle';
        case 'LOCKER':
          return 'fas fa-lock';
        case 'CAFETERIA':
          return 'fas fa-coffee';
        case 'PRINTER':
          return 'fas fa-print';
        case 'VENDING_MACHINE':
          return 'ni icon-snacks';
        case 'AIR_CONDITIONING':
          return 'fas fa-snowflake';

        default:
          return 'fas fa-question'; 
      }
    },
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
