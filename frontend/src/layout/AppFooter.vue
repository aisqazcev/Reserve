<template>
    <footer class="footer has-cards">
        <div class="container">
            <div class="row row-grid align-items-center my-md">
                <div class="col-lg-6">
                    <h3 class="text-primary font-weight-light mb-2">¡Gracias por reservar con nosotros!</h3>
                    <h4 class="mb-0 font-weight-light">No te quedes sin tu sitio.</h4>
                </div>
                <div class="col-lg-6 text-center">
                    <!-- <div>
                        <img src="img/logo_ejemplo.png" alt="Logo" style="max-width: 100%; height: auto;">
                    </div> -->
                </div>
            </div>
            <hr>
            <div class="row align-items-center justify-content-md-between">
                <div class="col-md-6 text-center mx-auto">
                    <ul class="nav nav-footer justify-content-end">
                        <li class="nav-item">
                            <a href="https://www.creative-tim.com" class="nav-link" target="_blank" rel="noopener">Información general</a>
                        </li>
                        <li class="nav-item">
                            <a href="https://www.creative-tim.com/presentation" class="nav-link" target="_blank" rel="noopener">FAQ</a>
                        </li>
                        <li class="nav-item">
                            <a href="http://blog.creative-tim.com" class="nav-link" target="_blank" rel="noopener">Política de privacidad</a>
                        </li>
                        <li class="nav-item">
                            <a href="http://blog.creative-tim.com" class="nav-link" target="_blank" rel="noopener">Contacto</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>
</template>
<script>
export default {
  name: 'app-footer',
  data() {
    return {
      year: new Date().getFullYear()
    }
  }
};
</script>
<style>
</style>
