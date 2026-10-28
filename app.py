"""
MVP - Salas de estudio Ad Portas (Grupo 2, Introducción a los Sistemas Inteligentes)
Ejecutar:  python -m streamlit run app.py

Tarea central: que un estudiante vea qué salas están libres AHORA (según
sensor + reservas) y reserve la que mejor se ajusta a su grupo.
Los sensores son SIMULADOS desde la barra lateral (no hay hardware en el MVP).
"""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st

import logica as lg

ZONA = ZoneInfo("America/Bogota")
CARPETA = Path(__file__).parent / "data"
ARCHIVO_SALAS = CARPETA / "salas.csv"
ARCHIVO_RESERVAS = CARPETA / "reservas.json"
ARCHIVO_SENSORES = CARPETA / "sensores.json"

ICONOS = {
    "Libre": "🟢 Libre",
    "Ocupada sin reserva": "🔴 Ocupada sin reserva",
    "En uso (reservada)": "🔴 En uso (reservada)",
    "Reservada (esperando llegada)": "🟡 Reservada (esperando llegada)",
    "No-show: se puede liberar": "🟠 No-show: se liberará",
}


# ------------------------------------------------------------ datos (archivos)
def cargar_salas():
    with open(ARCHIVO_SALAS, encoding="utf-8") as f:
        return [{
            "id": fila["id"], "nombre": fila["nombre"], "piso": int(fila["piso"]),
            "capacidad": int(fila["capacidad"]),
            "tablero": fila["tablero"] == "1", "pantalla": fila["pantalla"] == "1",
        } for fila in csv.DictReader(f)]


def cargar_reservas():
    if not ARCHIVO_RESERVAS.exists():
        return []
    try:
        datos = json.loads(ARCHIVO_RESERVAS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        st.warning("El archivo de reservas estaba dañado; se reinició.")
        return []
    for r in datos:
        r["inicio"] = datetime.fromisoformat(r["inicio"])
        r["fin"] = datetime.fromisoformat(r["fin"])
    return datos


def guardar_reservas(reservas):
    datos = [{**r, "inicio": r["inicio"].isoformat(), "fin": r["fin"].isoformat()}
             for r in reservas]
    ARCHIVO_RESERVAS.write_text(json.dumps(datos, ensure_ascii=False, indent=2),
                                encoding="utf-8")


def cargar_sensores(salas):
    if ARCHIVO_SENSORES.exists():
        try:
            return json.loads(ARCHIVO_SENSORES.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {s["id"]: False for s in salas}


def guardar_sensores(sensores):
    ARCHIVO_SENSORES.write_text(json.dumps(sensores), encoding="utf-8")


def hora(dt):
    return dt.strftime("%I:%M %p").lstrip("0")


# ------------------------------------------------------------ página
st.set_page_config(page_title="Salas Ad Portas", page_icon="📚", layout="centered")
st.title("📚 Salas de estudio Ad Portas")
st.write("Mira qué salas están libres **ahora** y reserva la que mejor se ajusta a tu grupo.")

salas = cargar_salas()
salas_por_id = {s["id"]: s for s in salas}
capacidad_max = max(s["capacidad"] for s in salas)
sensores = cargar_sensores(salas)

# ---------------- barra lateral: reloj de prueba + simulador de sensores
with st.sidebar:
    st.header("⚙️ Panel de pruebas")
    st.caption("Solo para la demostración del MVP. En el sistema real, "
               "estos datos vendrían de los sensores instalados en cada sala.")
    usar_hora_manual = st.toggle("Usar hora manual (para pruebas)")
    ahora_real = datetime.now(ZONA).replace(tzinfo=None, second=0, microsecond=0)
    if usar_hora_manual:
        h = st.time_input("Hora simulada", value=ahora_real.time(), step=300)
        ahora = datetime.combine(ahora_real.date(), h)
    else:
        ahora = ahora_real
    st.write(f"Hora usada: **{hora(ahora)}**")

    st.subheader("Sensores (simulados)")
    cambio = False
    for s in salas:
        valor = st.checkbox(f"Presencia en {s['nombre']}",
                            value=sensores.get(s["id"], False), key=f"sen_{s['id']}")
        if valor != sensores.get(s["id"], False):
            sensores[s["id"]] = valor
            cambio = True
    if cambio:
        guardar_sensores(sensores)

# ---------------- regla R3: liberar no-shows antes de mostrar nada
reservas = cargar_reservas()
reservas, liberadas = lg.liberar_no_shows(reservas, sensores, ahora)
guardar_reservas(reservas)
for r in liberadas:
    st.toast(f"{salas_por_id[r['sala_id']]['nombre']} se liberó: la reserva de "
             f"{r['alias']} no se usó en {lg.TOLERANCIA_MIN} minutos.", icon="🟠")

tab_ver, tab_reservar, tab_mis = st.tabs(["Disponibilidad ahora", "Reservar", "Reservas de hoy"])

# ---------------- pestaña 1: disponibilidad
with tab_ver:
    estados = {s["id"]: lg.estado_sala(s["id"], ahora, reservas, sensores.get(s["id"], False))
               for s in salas}
    libres = sum(1 for e in estados.values() if e == "Libre")
    st.metric("Salas libres en este momento", f"{libres} de {len(salas)}")
    for piso in sorted({s["piso"] for s in salas}):
        st.markdown(f"**Piso {piso}**")
        for s in [x for x in salas if x["piso"] == piso]:
            extras = []
            if s["tablero"]:
                extras.append("tablero")
            if s["pantalla"]:
                extras.append("pantalla")
            proxima = sorted([r for r in reservas if r["sala_id"] == s["id"] and r["inicio"] > ahora],
                             key=lambda r: r["inicio"])
            nota = f" · próxima reserva {hora(proxima[0]['inicio'])}" if proxima else ""
            st.write(f"{ICONOS[estados[s['id']]]} — **{s['nombre']}** "
                     f"({s['capacidad']} personas{', ' + ', '.join(extras) if extras else ''}){nota}")
    st.caption("🟢 libre · 🟡 reservada, esperando que llegue el grupo · 🔴 ocupada · "
               f"🟠 nadie llegó en {lg.TOLERANCIA_MIN} min: se libera")

# ---------------- pestaña 2: reservar
with tab_reservar:
    st.write("Indica tu grupo y te sugerimos la sala más adecuada.")
    with st.form("buscar"):
        alias = st.text_input("Nombre o alias del grupo", max_chars=40,
                              help="No uses datos personales como cédula o teléfono.")
        col1, col2 = st.columns(2)
        personas = col1.number_input("Número de personas", min_value=1,
                                     max_value=20, value=2, step=1)
        duracion = col2.selectbox("Duración", lg.DURACIONES_PERMITIDAS,
                                  index=1, format_func=lambda m: f"{m} min")
        inicio_hora = st.time_input("Hora de inicio",
                                    value=(ahora + timedelta(minutes=5)).time(), step=900)
        col3, col4 = st.columns(2)
        tablero = col3.checkbox("Necesito tablero")
        pantalla = col4.checkbox("Necesito pantalla")
        buscar = st.form_submit_button("Buscar sala")

    if buscar:
        inicio = datetime.combine(ahora.date(), inicio_hora)
        errores = lg.validar_solicitud(alias, int(personas), inicio, duracion, ahora, capacidad_max)
        if errores:
            for e in errores:
                st.error(e)
            st.session_state.pop("busqueda", None)
        else:
            opciones = lg.recomendar_salas(salas, reservas, sensores, int(personas),
                                           inicio, duracion, ahora, tablero, pantalla)
            st.session_state.busqueda = {
                "alias": alias, "personas": int(personas), "inicio": inicio,
                "duracion": duracion, "opciones": [o["id"] for o in opciones],
            }

    b = st.session_state.get("busqueda")
    if b:
        fin = b["inicio"] + timedelta(minutes=b["duracion"])
        if not b["opciones"]:
            st.warning(f"No hay salas que cumplan lo pedido de {hora(b['inicio'])} a {hora(fin)}. "
                       "Prueba otra hora, menos requisitos o una duración más corta.")
        else:
            mejor = salas_por_id[b["opciones"][0]]
            st.success(f"Sugerencia: **{mejor['nombre']}** (piso {mejor['piso']}, "
                       f"{mejor['capacidad']} puestos) de {hora(b['inicio'])} a {hora(fin)}.")
            st.caption("¿Por qué esta sala? Es la más pequeña que alcanza para tu grupo, "
                       "no tiene reservas que se crucen y, si es para ya, el sensor no "
                       "detecta a nadie adentro. Así las salas grandes quedan para grupos grandes.")
            elegida = st.selectbox("Sala a reservar", b["opciones"],
                                   format_func=lambda i: f"{salas_por_id[i]['nombre']} "
                                                         f"({salas_por_id[i]['capacidad']} puestos)")
            if st.button("Confirmar reserva", type="primary"):
                actuales = cargar_reservas()     # releer por si alguien reservó antes
                if lg.hay_choque(actuales, elegida, b["inicio"], fin):
                    st.error("Alguien acaba de reservar esa sala en ese horario. Busca de nuevo.")
                else:
                    actuales.append(lg.crear_reserva(b["alias"], elegida, b["inicio"],
                                                     b["duracion"], b["personas"]))
                    guardar_reservas(actuales)
                    st.session_state.pop("busqueda")
                    st.success(f"Reserva confirmada en {salas_por_id[elegida]['nombre']}. "
                               f"Tienes {lg.TOLERANCIA_MIN} minutos de tolerancia para llegar.")
                    st.rerun()

# ---------------- pestaña 3: reservas de hoy
with tab_mis:
    hoy = sorted([r for r in reservas if r["fin"] > ahora], key=lambda r: r["inicio"])
    if not hoy:
        st.info("No hay reservas vigentes.")
    for i, r in enumerate(hoy):
        c1, c2 = st.columns([4, 1])
        c1.write(f"**{r['alias']}** · {salas_por_id[r['sala_id']]['nombre']} · "
                 f"{hora(r['inicio'])}–{hora(r['fin'])} · {r['personas']} pers.")
        if c2.button("Cancelar", key=f"cancel_{i}"):
            restantes = [x for x in reservas if x is not r]
            guardar_reservas(restantes)
            st.rerun()

st.divider()
st.caption("Prototipo educativo · Grupo 2 · Los sensores y la lista de salas son simulados; "
           "las reglas deben validarse con usuarios reales de Ad Portas.")
