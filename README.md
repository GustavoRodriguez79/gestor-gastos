# 💰 Gestor de Gastos Personales

API REST para registrar y gestionar gastos personales, con frontend en HTML/CSS/JS.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.137-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql)
![Estado](https://img.shields.io/badge/Estado-Completo-brightgreen)

---

## 📸 Vista previa

### Tema oscuro
![Tema oscuro](docs/images/tema-oscuro.png)

### Tema claro
![Tema claro](docs/images/tema-claro.png)

---

## 🚀 Tecnologías

- **Backend:** Python · FastAPI · uvicorn
- **Base de datos:** PostgreSQL · psycopg2
- **Frontend:** HTML · CSS · JavaScript vanilla
- **Otros:** python-dotenv · Pydantic

---

## 📁 Estructura del proyecto

```
gestor-gastos/
├── backend/
│   ├── main.py          # Entrada de la app FastAPI
│   ├── database.py      # Conexión a PostgreSQL
│   ├── models.py        # Schemas Pydantic
│   └── routes/
│       └── gastos.py    # Endpoints CRUD
├── frontend/
│   ├── index.html       # Interfaz de usuario
│   ├── style.css        # Estilos con tema oscuro/claro
│   └── app.js           # Lógica y fetch a la API
├── docs/
│   └── images/          # Capturas de pantalla
├── .gitignore
└── README.md
```

---

## 🗄️ Base de datos

```sql
CREATE TABLE gastos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/gastos` | Obtener todos los gastos |
| GET | `/gastos?mes=6&anio=2026` | Filtrar por mes y año |
| POST | `/gastos` | Crear un gasto nuevo |
| PUT | `/gastos/{id}` | Actualizar un gasto |
| DELETE | `/gastos/{id}` | Eliminar un gasto |
| GET | `/gastos/resumen` | Resumen del mes actual |

Documentación interactiva disponible en `http://127.0.0.1:8000/docs`

---
## 🏗️ Arquitectura

```mermaid
flowchart TD
    subgraph FE["Frontend - HTML · CSS · JavaScript"]
        A["index.html - Estructura visual"]
        B["style.css - Estilos y diseño"]
        C["app.js - Fetch a la API"]
    end

    subgraph API["Backend - FastAPI · Python · uvicorn"]
        D["main.py - App · CORS · routers"]
        E["models.py - Pydantic schemas"]
        F["database.py - Conexion psycopg2"]
        G["routes/gastos.py - GET · POST · PUT · DELETE"]
    end

    subgraph DB["Base de datos - PostgreSQL"]
        H["tabla gastos - id · monto · categoria · fecha"]
        I[".env - Credenciales"]
    end

    C -->|HTTP JSON| G
    G -->|JSON response| C
    D --> G
    E --> G
    F --> G
    G -->|SQL Queries| H
    I -.->|variables de entorno| F

    classDef frontend fill:#1a3a5c,stroke:#38bdf8,color:#e2e8f0
    classDef backend fill:#1a3a2a,stroke:#00E676,color:#e2e8f0
    classDef database fill:#3a1a1a,stroke:#f87171,color:#e2e8f0

    class A,B,C frontend
    class D,E,F,G backend
    class H,I database
```
---

## ⚙️ Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/GustavoRodriguez79/gestor-gastos.git
cd gestor-gastos
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install fastapi uvicorn psycopg2-binary python-dotenv
```

### 3. Configurar variables de entorno

Crear un archivo `backend/.env` con tus credenciales:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestor_gastos
DB_USER=postgres
DB_PASSWORD=tu_contraseña
```

### 4. Crear la base de datos

Ejecutar el SQL de la sección Base de datos en pgAdmin.

### 5. Correr el servidor

```bash
cd backend
uvicorn main:app --reload
```

### 6. Abrir el frontend

Abrís `frontend/index.html` con Live Server en VS Code.

---

## ✨ Funcionalidades

- Registrar gastos con descripción, monto, categoría y fecha
- Listar todos los gastos ordenados por fecha
- Filtrar gastos por mes y año
- Eliminar gastos con confirmación
- Resumen del mes: total gastado y categoría con mayor gasto
- Tema oscuro y claro con toggle — preferencia guardada en localStorage
- Diseño responsive para móvil y escritorio

---

## 👤 Autor

**Gustavo Ariel Rodriguez**
Tecnicatura Universitaria en Programación — UTN San Rafael
[GitHub](https://github.com/GustavoRodriguez79) · [LinkedIn](https://www.linkedin.com/in/gustavo-ariel-rodr%C3%ADguez-fornes-36a899370/) · [garodrifornes79@gmail.com](mailto:garodrifornes79@gmail.com)