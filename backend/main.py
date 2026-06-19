# main.py
# Punto de entrada principal de la aplicación FastAPI.
# Aquí se inicializa la app, se configuran los middlewares
# y se registran las rutas (routers).

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.gastos import router as gastos_router

# Inicialización de la aplicación FastAPI con metadata
app = FastAPI(
    title="Gestor de Gastos Personales",
    description="API REST para registrar y gestionar gastos personales.",
    version="1.0.0"
)

# Configuración de CORS (Cross-Origin Resource Sharing)
# Permite que el frontend (HTML/JS) pueda comunicarse con la API
# aunque estén corriendo en puertos distintos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # En producción se reemplaza por el dominio real
    allow_methods=["*"],        # Permite GET, POST, PUT, DELET, etc
    allow_headers=["*"],        # Permite todos los headers
)

# Registro del router de gastos con prefijo / gastos
# Todas las rutas definidas en gastos.py van a empezar con /gastos
app.include_router(gastos_router, prefix="/gastos", tags=["Gastos"])

# Ruta raíz para verificar que la API está corriendo
@app.get("/")
def root():
    """
    Endpoint de bienvenida.
    Útil para verificar que el servidor está activo. 
    """
    return {"mensaje": "API Gestor de Gastos funcionando correctamente"}


