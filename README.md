# SeatEasy
## Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)
- [Agradecimientos](#agradecimientos)

## Descripción del Proyecto
Es una aplicación diseñada para la gestión de reservas de asientos en salas de estudio. El objetivo del proyecto es optimizar la experiencia del usuario al permitir la reserva anticipada de asientos y proporcionar información en tiempo real sobre la disponibilidad y el equipamiento de las salas.

La aplicación está construida utilizando Django para el backend y Argon Vue para el frontend, asegurando una arquitectura robusta y una experiencia de usuario intuitiva.

## Instalación
Para instalar y ejecutar el proyecto, sigue estos pasos:

### Pre-requisitos
Asegúrate de tener instaladas las siguientes herramientas en tu sistema:

- **Python** (versión 3.10.9)
- **Node.js** (versión 19.7.0) y **npm**
- **Git**

### Clonación y Configuración del Proyecto

1. Clona el repositorio:
    ```bash
    git clone https://github.com/aisqazcev/Reserve.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd .\backend\
    ```

### Configuración del Backend

3. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

4. Instala las dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```

5. Configura las variables de entorno para el backend (copia el archivo `.env.example` a `.env` y ajusta según sea necesario):
    ```bash
    cp .env.example .env
    ```

6. Realiza las migraciones de la base de datos:
   ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```

### Configuración del Frontend

7. Instala las dependencias de Node.js:
    ```bash
    npm install
    ```

### Inicio de la Aplicación

8. Inicia el servidor de desarrollo de Django:
    ```bash
    python manage.py runserver
    ```

9. Inicia el servidor de desarrollo de Vue:
    ```bash
    npm run serve
    ```

### Acceso a la Aplicación

10. Accede a la interfaz web a través de tu navegador en `http://localhost:8000`.

## Archivos Necesarios

Asegúrate de que los siguientes archivos están presentes en tu repositorio:

- `requirements.txt`: Lista de dependencias de Python.
- `package.json`: Lista de dependencias de Node.js.
- `.env.example`: Archivo de ejemplo para configuración de variables de entorno.



