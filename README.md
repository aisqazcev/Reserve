# SeatEasy
## Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Despliegue](#despliegue)

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
### Configuración del Backend
2. Navega al directorio del proyecto:
    ```bash
    cd backend
    ```
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
7. Navega al directorio del proyecto:
    ```bash
    cd frontend
    ```
8. Instala las dependencias de Node.js:
    ```bash
    npm install
    ```

### Inicio de la Aplicación

9. Inicia el servidor de desarrollo de Django desde la carpeta backend:
    ```bash
    python manage.py runserver
    ```

9. Inicia el servidor de desarrollo de Vue desde la carpeta frontend:
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

## Uso

Para utilizar la aplicación:

1. Accede a la interfaz web a través de tu navegador en `http://localhost:8000`.
2. Regístrate o inicia sesión.
3. Navega por las salas disponibles y realiza una reserva.
4. Utiliza las funciones de reporte de incidencias e invitaciones para mejorar tu experiencia.

## Tecnologías Utilizadas

- **Backend**: Django
- **Frontend**: Argon Vue
- **Base de Datos**: SQLite (puede ser configurado para usar PostgreSQL, MySQL, etc.)
- **Control de Versiones**: Git

## Despliegue
### Frontend (Vue.js con Firebase Hosting)

Para desplegar el frontend:

1. Desde el directorio del frontend:
   ```bash
   npm run build
   ```
   
2. Una vez que el proyecto está construido, despliégalo usando Firebase:
   ```bash
   firebase deploy
   ```

### Backend (Django con Azure)
   ```bash
   az webapp up --runtime PYTHON:3.10 --logs --sku B1 --location westus
   ```
Asegúrate de tener instalado Azure CLI (az) y haber iniciado sesión en tu cuenta de Azure antes de ejecutar este comando.
Este comando desplegará la aplicación Django en Azure Web Apps utilizando Python 3.10 como entorno de ejecución.
