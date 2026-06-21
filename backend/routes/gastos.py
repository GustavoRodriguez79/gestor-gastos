# routes/gastos.py
# Define todos los endpoints de la API para el recurso "gastos".
# Cada función maneja una operación distinta sobre la base de datos.

from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import date
from models import GastoCreate, GastoUpdate, GastoResponse
from database import get_connection

# APIRouter permite organizar las rutas en módulos separados
# Se registra en main.py con el prefijo /gastos
router = APIRouter()


@router.get("/")
def obtener_gastos(mes: Optional[int] = None, anio: Optional[int] = None):
    """
    Retorna todos los gastos.
    Si se pasan los parámetros mes y anio, filtra por ese período.
    Ejemplo: GET /gastos?mes=6&anio=2026
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if mes and anio:
            # Filtra gastos por mes y año usando EXTRACT de PostgreSQL
            cursor.execute("""
                SELECT id, descripcion, monto, categoria, fecha, created_at
                FROM gastos
                WHERE EXTRACT(MONTH FROM fecha) = %s
                AND EXTRACT(YEAR FROM fecha) = %s
                ORDER BY fecha DESC
            """, (mes, anio))
        else:
            # Sin filtros trae todos los gastos ordenados por fecha
            cursor.execute("""
                SELECT id, descripcion, monto, categoria, fecha, created_at
                FROM gastos
                ORDER BY fecha DESC
            """)

        filas = cursor.fetchall()

        # Convierte cada fila en un diccionario para retornar como JSON
        gastos = []
        for fila in filas:
            gastos.append({
                "id": fila[0],
                "descripcion": fila[1],
                "monto": float(fila[2]),
                "categoria": fila[3],
                "fecha": str(fila[4]),
                "created_at": str(fila[5])
            })
        return gastos

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Siempre se cierra el cursor y la conexión aunque haya error
        cursor.close()
        conn.close()

@router.get("/resumen")
def obtener_resumen(mes: Optional[int] = None, anio: Optional[int] = None):
    """
    Retorna un resumen del mes actual o del mes/año indicado.
    Incluye: total gastado y la categoría con mayor gasto.
    Ejemplo: GET /gastos/resumen?mes=6&anio=2026
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Si no se pasan parámetros usa el mes y año actuales
        hoy = date.today()
        mes = mes or hoy.month
        anio = anio or hoy.year

        # Total gastado en el período
        cursor.execute("""
            SELECT COALESCE(SUM(monto), 0)
            FROM gastos
            WHERE EXTRACT(MONTH FROM fecha) = %s
            AND EXTRACT(YEAR FROM fecha) = %s
        """, (mes, anio))
        total = float(cursor.fetchone()[0])

        # Categoría con mayor gasto en el período
        cursor.execute("""
            SELECT categoria, SUM(monto) as total_categoria
            FROM gastos
            WHERE EXTRACT(MONTH FROM fecha) = %s
            AND EXTRACT(YEAR FROM fecha) = %s
            GROUP BY categoria
            ORDER BY total_categoria DESC
            LIMIT 1
        """, (mes, anio))

        fila = cursor.fetchone()
        categoria_top = fila[0] if fila else "Sin gastos"
        total_categoria_top = float(fila[1]) if fila else 0

        return {
            "mes": mes,
            "anio": anio,
            "total_gastado": total,
            "categoria_top": categoria_top,
            "total_categoria_top": total_categoria_top
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/", status_code=201)
def crear_gasto(gasto: GastoCreate):
    """
    Crea un nuevo gasto en la base de datos.
    Recibe los datos validados por Pydantic desde el body del request.
    Retorna el id del gasto creado.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO gastos (descripcion, monto, categoria, fecha)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (gasto.descripcion, gasto.monto, gasto.categoria, gasto.fecha))

        # RETURNING id nos devuelve el id generado automáticamente
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        return {"mensaje": "Gasto creado correctamente", "id": nuevo_id}

    except Exception as e:
        conn.rollback()  # Revierte la operación si algo falla
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.put("/{gasto_id}")
def actualizar_gasto(gasto_id: int, gasto: GastoUpdate):
    """
    Actualiza uno o más campos de un gasto existente.
    Solo modifica los campos que se envíen en el body.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Construye dinámicamente solo los campos que llegaron con valor
        campos = []
        valores = []

        if gasto.descripcion is not None:
            campos.append("descripcion = %s")
            valores.append(gasto.descripcion)
        if gasto.monto is not None:
            campos.append("monto = %s")
            valores.append(gasto.monto)
        if gasto.categoria is not None:
            campos.append("categoria = %s")
            valores.append(gasto.categoria)
        if gasto.fecha is not None:
            campos.append("fecha = %s")
            valores.append(gasto.fecha)

        # Si no se envió ningún campo, no hay nada que actualizar
        if not campos:
            raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

        valores.append(gasto_id)  # El id va al final para el WHERE

        query = f"UPDATE gastos SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(query, valores)

        # rowcount indica cuántas filas fueron afectadas
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")

        conn.commit()
        return {"mensaje": "Gasto actualizado correctamente"}

    except HTTPException:
        raise  # Re-lanza las HTTPException sin atraparlas
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/{gasto_id}")
def eliminar_gasto(gasto_id: int):
    """
    Elimina un gasto por su id.
    Retorna 404 si el gasto no existe.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM gastos WHERE id = %s", (gasto_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")

        conn.commit()
        return {"mensaje": "Gasto eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()



        