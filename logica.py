"""
Lógica del MVP "Salas Ad Portas" (Grupo 2 - Introducción a los Sistemas Inteligentes).

Este módulo NO depende de Streamlit: contiene solo las reglas de decisión,
para poder probarlas por separado (ver test_logica.py).

Componente "inteligente" del MVP = reglas explicables que combinan dos fuentes:
  1) El sensor de presencia de cada sala (en el MVP es SIMULADO).
  2) Las reservas registradas en el sistema.

Reglas:
  R1. Estado de la sala:
      - sensor libre  + sin reserva activa  -> "Libre"
      - sensor ocupado + sin reserva activa -> "Ocupada sin reserva"
      - sensor ocupado + reserva activa     -> "En uso (reservada)"
      - sensor libre  + reserva activa, dentro de la tolerancia -> "Reservada (esperando llegada)"
      - sensor libre  + reserva activa, pasada la tolerancia    -> "No-show: se puede liberar"
  R2. Recomendación: entre las salas sin choque de horario, con capacidad
      suficiente y libres según el sensor (si la reserva es para ya), se
      sugiere la de MENOR capacidad que alcance (para no desperdiciar salas
      grandes con grupos pequeños).
  R3. No-show: si una reserva lleva más de TOLERANCIA_MIN minutos iniciada y el
      sensor nunca detecta presencia, la reserva se libera automáticamente.
"""

from datetime import datetime, timedelta

HORA_APERTURA = 7     # 7:00 a. m.  (supuesto del equipo, validar con Ad Portas)
HORA_CIERRE = 21      # 9:00 p. m.
DURACIONES_PERMITIDAS = (30, 60, 90, 120)   # minutos
TOLERANCIA_MIN = 10   # minutos para llegar antes de liberar la sala


# ---------------------------------------------------------------- utilidades
def se_cruzan(inicio_a, fin_a, inicio_b, fin_b):
    """True si dos intervalos [inicio, fin) se superponen."""
    return inicio_a < fin_b and inicio_b < fin_a


def reservas_de_sala(reservas, sala_id):
    return [r for r in reservas if r["sala_id"] == sala_id]


def reserva_activa(reservas, sala_id, ahora):
    """Devuelve la reserva que está en curso en la sala, o None."""
    for r in reservas_de_sala(reservas, sala_id):
        if r["inicio"] <= ahora < r["fin"]:
            return r
    return None


def hay_choque(reservas, sala_id, inicio, fin):
    return any(se_cruzan(inicio, fin, r["inicio"], r["fin"])
               for r in reservas_de_sala(reservas, sala_id))


# ---------------------------------------------------------------- R1: estado
def estado_sala(sala_id, ahora, reservas, sensor_ocupado):
    r = reserva_activa(reservas, sala_id, ahora)
    if r is None:
        return "Ocupada sin reserva" if sensor_ocupado else "Libre"
    if sensor_ocupado:
        return "En uso (reservada)"
    if ahora - r["inicio"] <= timedelta(minutes=TOLERANCIA_MIN):
        return "Reservada (esperando llegada)"
    return "No-show: se puede liberar"


# ---------------------------------------------------------------- validación
def validar_solicitud(alias, personas, inicio, duracion, ahora, capacidad_max):
    """Devuelve una lista de mensajes de error (vacía si todo está bien)."""
    errores = []
    if not alias or not alias.strip():
        errores.append("Escribe un nombre o alias para identificar la reserva.")
    elif len(alias.strip()) > 40:
        errores.append("El alias no puede tener más de 40 caracteres.")
    if personas < 1:
        errores.append("El grupo debe tener al menos 1 persona.")
    elif personas > capacidad_max:
        errores.append(f"Ninguna sala admite {personas} personas "
                       f"(máximo {capacidad_max}). Divide el grupo.")
    if duracion not in DURACIONES_PERMITIDAS:
        errores.append("La duración debe ser 30, 60, 90 o 120 minutos.")
    fin = inicio + timedelta(minutes=duracion)
    if inicio < ahora - timedelta(minutes=5):
        errores.append("La hora de inicio ya pasó. Elige una hora futura.")
    if inicio.date() != ahora.date():
        errores.append("En este MVP solo se reserva para el día de hoy.")
    if inicio.hour < HORA_APERTURA or (fin.hour, fin.minute) > (HORA_CIERRE, 0) \
            or fin.date() != inicio.date():
        errores.append(f"La reserva debe estar entre las {HORA_APERTURA}:00 "
                       f"y las {HORA_CIERRE}:00.")
    return errores


# ---------------------------------------------------------------- R2: recomendar
def recomendar_salas(salas, reservas, sensores, personas, inicio, duracion,
                     ahora, requiere_tablero=False, requiere_pantalla=False):
    """Devuelve las salas que sirven, ordenadas de mejor a peor ajuste."""
    fin = inicio + timedelta(minutes=duracion)
    es_para_ya = inicio <= ahora + timedelta(minutes=5)
    candidatas = []
    for s in salas:
        if s["capacidad"] < personas:
            continue
        if requiere_tablero and not s["tablero"]:
            continue
        if requiere_pantalla and not s["pantalla"]:
            continue
        if hay_choque(reservas, s["id"], inicio, fin):
            continue
        # Si la reserva es para ya, el sensor debe confirmar que está vacía.
        if es_para_ya and sensores.get(s["id"], False):
            continue
        candidatas.append(s)
    # Mejor ajuste: menor capacidad sobrante; desempate por piso más bajo.
    return sorted(candidatas, key=lambda s: (s["capacidad"] - personas, s["piso"]))


# ---------------------------------------------------------------- R3: no-shows
def liberar_no_shows(reservas, sensores, ahora):
    """Quita reservas iniciadas hace más de TOLERANCIA_MIN sin presencia.
    Devuelve (reservas_vigentes, reservas_liberadas)."""
    vigentes, liberadas = [], []
    for r in reservas:
        empezo_hace = ahora - r["inicio"]
        sin_presencia = not sensores.get(r["sala_id"], False)
        en_curso = r["inicio"] <= ahora < r["fin"]
        if en_curso and sin_presencia and r.get("llego") is not True \
                and empezo_hace > timedelta(minutes=TOLERANCIA_MIN):
            liberadas.append(r)
        else:
            if en_curso and not sin_presencia:
                r["llego"] = True   # el sensor confirmó la llegada
            vigentes.append(r)
    return vigentes, liberadas


def crear_reserva(alias, sala_id, inicio, duracion, personas):
    return {
        "alias": alias.strip(),
        "sala_id": sala_id,
        "inicio": inicio,
        "fin": inicio + timedelta(minutes=duracion),
        "personas": int(personas),
        "llego": False,
    }
