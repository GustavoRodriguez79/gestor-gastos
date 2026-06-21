// app.js
// Lógica principal del frontend.
// Se comunica con la API de FastAPI usando fetch.

// ─── URL base de la API ───
const API_URL = "http://127.0.0.1:8000/gastos";

// ─── Al cargar la página ───
document.addEventListener("DOMContentLoaded", () => {
    cargarGastos();
    cargarResumen();
    establecerFechaHoy();
    inicializarTema();
});

// ══════════════════════════════════════════
//  TEMA OSCURO / CLARO
// ══════════════════════════════════════════

function inicializarTema() {
    // Recupera el tema guardado en localStorage, o usa oscuro por defecto
    const temaGuardado = localStorage.getItem("tema") || "dark";
    aplicarTema(temaGuardado);
}

function aplicarTema(tema) {
    const html = document.documentElement;
    const icono = document.querySelector("#theme-toggle i");
    const label = document.getElementById("theme-label");

    html.setAttribute("data-theme", tema);
    localStorage.setItem("tema", tema);

    // Cambia el icono y el texto según el tema activo
    if (tema === "dark") {
        icono.className = "fas fa-moon";
        label.textContent = "Tema claro";
    } else {
        icono.className = "fas fa-sun";
        label.textContent = "Tema oscuro";
    }
}

// Evento: botón toggle de tema
document.getElementById("theme-toggle").addEventListener("click", () => {
    const temaActual = document.documentElement.getAttribute("data-theme");
    const nuevoTema = temaActual === "dark" ? "light" : "dark";
    aplicarTema(nuevoTema);
});

// ══════════════════════════════════════════
//  UTILIDADES
// ══════════════════════════════════════════

// Establece la fecha de hoy como valor por defecto en el input fecha
function establecerFechaHoy() {
    const hoy = new Date().toISOString().split("T")[0];
    document.getElementById("fecha").value = hoy;
}

// Limpia el formulario después de agregar un gasto
function limpiarFormulario() {
    document.getElementById("descripcion").value = "";
    document.getElementById("monto").value = "";
    document.getElementById("categoria").value = "";
    establecerFechaHoy();
}

// ══════════════════════════════════════════
//  CARGAR Y RENDERIZAR GASTOS
// ══════════════════════════════════════════

// Obtiene los gastos de la API y los muestra en la tabla
async function cargarGastos(mes = null, anio = null) {
    try {
        // Construye la URL con filtros opcionales
        let url = API_URL;
        if (mes && anio) {
            url += `?mes=${mes}&anio=${anio}`;
        }

        const respuesta = await fetch(url);

        if (!respuesta.ok) throw new Error("Error al obtener gastos");

        const gastos = await respuesta.json();
        renderizarTabla(gastos);
    } catch (error) {
        console.error("Error al cargar gastos:", error);
        mostrarMensajeTabla("Error al conectar con la API. Verificá que el servidor esté corriendo.");
    }
}

// Renderiza los gastos en la tabla del HTML
function renderizarTabla(gastos) {
    const tbody = document.getElementById("tabla-gastos");
    tbody.innerHTML = "";

    if (gastos.length === 0) {
        mostrarMensajeTabla("No hay gastos registrados.");
        return;
    }

    // Crea una fila por cada gasto recibido
    gastos.forEach(gasto => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${gasto.fecha}</td>
            <td>${gasto.descripcion}</td>
            <td>${gasto.categoria}</td>
            <td><strong>$${parseFloat(gasto.monto).toFixed(2)}</strong></td>
            <td>
                <button class="btn-eliminar" onclick="eliminarGasto(${gasto.id})">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </td>
        `;
        tbody.appendChild(fila);
    });
}

// Muestra un mensaje centrado en el cuerpo de la tabla
function mostrarMensajeTabla(mensaje) {
    const tbody = document.getElementById("tabla-gastos");
    tbody.innerHTML = `
        <tr>
            <td colspan="5" style="text-align:center; color: var(--text-secondary); padding: 30px;">
                ${mensaje}
            </td>
        </tr>
    `;
}

// ══════════════════════════════════════════
//  RESUMEN DEL MES
// ══════════════════════════════════════════

// Obtiene y muestra el resumen del mes actual
async function cargarResumen() {
    try {
        const respuesta = await fetch(`${API_URL}/resumen`);

        if (!respuesta.ok) throw new Error("Error al obtener resumen");

        const resumen = await respuesta.json();

        // Actualiza las cards del resumen
        document.getElementById("total-gastado").textContent =
            `$${resumen.total_gastado.toFixed(2)}`;
        document.getElementById("categoria-top").textContent =
            resumen.categoria_top;
    } catch (error) {
        console.error("Error al cargar resumen:", error);
    }
}

// ══════════════════════════════════════════
//  CREAR GASTO
// ══════════════════════════════════════════

async function crearGasto() {
    const descripcion = document.getElementById("descripcion").value.trim();
    const monto = document.getElementById("monto").value;
    const categoria = document.getElementById("categoria").value;
    const fecha = document.getElementById("fecha").value;

    // Validación antes de enviar
    if (!descripcion || !monto || !categoria || !fecha) {
        alert("Por favor completá todos los campos.");
        return;
    }

    if (parseFloat(monto) <= 0) {
        alert("El monto debe ser mayor a cero.");
        return;
    }

    try {
        const respuesta = await fetch(API_URL + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                descripcion,
                monto: parseFloat(monto),
                categoria,
                fecha
            })
        });

        if (respuesta.ok) {
            limpiarFormulario();
            cargarGastos();   // Recarga la tabla
            cargarResumen();  // Actualiza el resumen
        } else {
            alert("Error al crear el gasto. Intentá nuevamente.");
        }
    } catch (error) {
        console.error("Error al crear gasto:", error);
        alert("No se pudo conectar con la API.");
    }
}

// ══════════════════════════════════════════
//  ELIMINAR GASTO
// ══════════════════════════════════════════

async function eliminarGasto(id) {
    // Pide confirmación antes de eliminar
    if (!confirm("¿Estás seguro que querés eliminar este gasto?")) return;

    try {
        const respuesta = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (respuesta.ok) {
            cargarGastos();   // Recarga la tabla
            cargarResumen();  // Actualiza el resumen
        } else {
            alert("Error al eliminar el gasto.");
        }
    } catch (error) {
        console.error("Error al eliminar gasto:", error);
        alert("No se pudo conectar con la API.");
    }
}

// ══════════════════════════════════════════
//  EVENTOS
// ══════════════════════════════════════════

// Botón agregar gasto
document.getElementById("btn-agregar").addEventListener("click", crearGasto);

// Botón filtrar por mes y año
document.getElementById("btn-filtrar").addEventListener("click", () => {
    const mes = document.getElementById("filtro-mes").value;
    const anio = document.getElementById("filtro-anio").value;

    if (!mes || !anio) {
        alert("Seleccioná mes y año para filtrar.");
        return;
    }

    cargarGastos(mes, anio);
});

// Botón ver todos — limpia filtros y recarga
document.getElementById("btn-limpiar").addEventListener("click", () => {
    document.getElementById("filtro-mes").value = "";
    document.getElementById("filtro-anio").value = "";
    cargarGastos();
});