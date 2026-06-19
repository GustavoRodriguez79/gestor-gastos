# models.py
# Define los modelos de datos usando Pydantic.
# Pydantic valida automáticamente que los datos recibidos tengan
# el tipo y formato correcto antes de procesarlos

from pydantic import BaseModel
from datetime import date
from typing import Optional

class GastoBase(BaseModel):
    """
    Campos base compartidos entre creación y respuesta.
    Se reutiliza para no repetir código.
    """
    descripcion: str
    monto: float
    categoria: str
    fecha: date

class GastoCreate(GastoBase):
    """
    Modelo usado al crear un gasto nuevo (POST).
    Hereda todo los campos de GastoBase.
    No incluye el id porque lo genera la base de datos automáticamente.
    """
    pass 

class GastoUpdate(BaseModel):
    """
    Modelo usado al editar un gasto (PUT).
    Todos los campos son opcionales para permitir
    actualizar solo los campos que se necesiten.    
    """
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    categoria: Optional[str] = None
    fecha: Optional[date] = None

class GastoResponse(GastoBase):
    """
    Modelo usado en las respuestas de la API (GET).
    Incluye el id y la fecha de creación que viene de la base de datos.
    """
    id: int
    created_at: str

    class Config:
        # Permite que Pydantic lea datos desde objetos de la base de datos
        # y no solo desde diccionarios
        from_attributes = True


