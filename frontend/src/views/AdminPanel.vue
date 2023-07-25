<template>
    <div class="admin-panel">
      <h1>Admin Panel</h1>
      <nav>
        <ul>
          <li><router-link to="/admin/locations">Manage Locations</router-link></li>
          <!-- Agregar aquí más enlaces a otras funcionalidades de administración -->
        </ul>
      </nav>
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminPanel',
  };
  </script>
  
  <style>
  /* Agrega estilos según tus preferencias */
  .admin-panel {
    padding: 20px;
  }
  h1 {
    text-align: center;
  }
  nav {
    margin-top: 20px;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin: 5px 0;
  }
  li a {
    text-decoration: none;
    color: #007BFF;
  }
  </style>
  