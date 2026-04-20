# Prode Mundial 2026 - API Backend

esto es ia hay que cambiarlo con nuestras palabras 

Este proyecto consiste en el desarrollo de una API REST para gestionar el fixture y los pronósticos deportivos (ProDe) del Mundial de la FIFA 2026. La aplicación está diseñada para fomentar la interacción entre colaboradores de una empresa con un fin solidario.

---

## Arquitectura del Proyecto

Para cumplir con los estándares de calidad de la cátedra, el proyecto implementa una arquitectura de **Separación de Responsabilidades** en tres capas principales. Esto facilita el mantenimiento, el testeo y evita el "código espagueti"

### 1. Capa de Routers (`/routes`)
* **Responsabilidad:** Punto de entrada de la API
* **Función:** Define los endpoints (rutas), recibe las request y se encarga del manejo de errores
* **Independencia:** No conoce la lógica de negocio ni realiza consultas SQL

### 2. Capa de Servicios (`/services`)
* **Responsabilidad:** Lógica de Negocio
* **Función:** Es el "cerebro" de la API. Valida que los datos recibidos tengan sentido lógico (ej: formatos de fecha, reglas del torneo) y orquesta la comunicación entre el Router y el Repositorio
* **Independencia:** No sabe nada sobre HTTP ni sobre la implementación específica de la base de datos

### 3. Capa de Repositorios (`/repositories`)
* **Responsabilidad:** Persistencia de datos.
* **Función:** Es la única capa que contiene sentencias SQL. Se encarga de abrir/cerrar conexiones, manejar cursores y transformar los resultados de la DB en estructuras de Python.
* **Independencia:** Solo se preocupa por almacenar y recuperar datos de forma eficiente.

---

## Instalación y Ejecucion

Sigue estos pasos para configurar tu entorno local:

### 1. Clonar y Preparar Entorno
```bash
# Clonar el repositorio (si aplica)
git clone <url-del-repo>

# Crear y activar entorno virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# Crear y activar entorno virtual (Linux/macOS)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Base de Datos

En `db.py` cambien la constante **PASSWORD** con la contraseña de su base de datos, luego:

```bash
# Crear la estructura de tablas (Database & Tables)
python init_db.py

# Poblar la base de datos con el fixture inicial
python seed.py
```

### 2. Ejecucion de la API 

```bash
python app.py
```
