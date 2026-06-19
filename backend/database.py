# database.py
# Módulo encargado de gestionar la conexión a la base de datos PostgresSQL
# Utiliza variables de entorno para no exponer credenciales en el código

import psycopg2
from dotenv import load_dotenv
import os

# Carga las variables definidas en el archivo .env
load_dotenv()

def get_connection():
    """
    Crea y retorna una conexión activa a la base de datos PostgresSQL.
    Las credenciales se leen desde las variables de entorno.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),           # Servidor de la base de datos
        port=os.getenv("DB_PORT"),           # Puerto (por defecto 5432 en PostgreSQL)
        dbname=os.getenv("DB_NAME"),         # Nombre de la base de datos
        user=os.getenv("DB_USER"),           # Usuario de PostgreSQL
        password=os.getenv("DB_PASSWORD")    # Contraseña del usuario
    )
