"""Pruebas automáticas de las reglas del MVP.  Ejecutar:  python -m unittest -v"""
import unittest
from datetime import datetime, timedelta

import logica as lg

AHORA = datetime(2026, 11, 3, 10, 0)
SALAS = [
    {"id": "S101", "nombre": "Sala 101", "piso": 1, "capacidad": 4, "tablero": True, "pantalla": False},
    {"id": "S102", "nombre": "Sala 102", "piso": 1, "capacidad": 6, "tablero": True, "pantalla": True},
    {"id": "S103", "nombre": "Sala 103", "piso": 1, "capacidad": 2, "tablero": False, "pantalla": False},
    {"id": "S202", "nombre": "Sala 202", "piso": 2, "capacidad": 8, "tablero": True, "pantalla": True},
]
SIN_SENSORES = {s["id"]: False for s in SALAS}


def reserva(sala, minutos_desde_ahora, duracion=60):
    return lg.crear_reserva("Grupo X", sala, AHORA + timedelta(minutes=minutos_desde_ahora), duracion, 2)


class TestValidacion(unittest.TestCase):
    def test_solicitud_valida(self):
        self.assertEqual(lg.validar_solicitud("Grupo 2", 3, AHORA + timedelta(minutes=10), 60, AHORA, 8), [])

    def test_alias_vacio(self):
        errores = lg.validar_solicitud("   ", 3, AHORA, 60, AHORA, 8)
        self.assertTrue(any("alias" in e for e in errores))

    def test_grupo_demasiado_grande(self):
        errores = lg.validar_solicitud("G", 9, AHORA, 60, AHORA, 8)
        self.assertTrue(any("Divide el grupo" in e for e in errores))

    def test_hora_pasada(self):
        errores = lg.validar_solicitud("G", 2, AHORA - timedelta(hours=1), 60, AHORA, 8)
        self.assertTrue(any("ya pasó" in e for e in errores))

    def test_limite_cierre_exacto_es_valido(self):
        inicio = AHORA.replace(hour=20, minute=0)   # 8:00 p. m. + 60 min = 9:00 p. m.
        self.assertEqual(lg.validar_solicitud("G", 2, inicio, 60, AHORA, 8), [])

    def test_pasa_del_cierre(self):
        inicio = AHORA.replace(hour=20, minute=30)
        errores = lg.validar_solicitud("G", 2, inicio, 60, AHORA, 8)
        self.assertTrue(any("21:00" in e for e in errores))


class TestEstado(unittest.TestCase):
    def test_libre(self):
        self.assertEqual(lg.estado_sala("S101", AHORA, [], False), "Libre")

    def test_ocupada_sin_reserva(self):
        self.assertEqual(lg.estado_sala("S101", AHORA, [], True), "Ocupada sin reserva")

    def test_reservada_esperando(self):
        self.assertEqual(lg.estado_sala("S101", AHORA, [reserva("S101", -5)], False),
                         "Reservada (esperando llegada)")

    def test_no_show(self):
        self.assertEqual(lg.estado_sala("S101", AHORA, [reserva("S101", -15)], False),
                         "No-show: se puede liberar")

    def test_en_uso(self):
        self.assertEqual(lg.estado_sala("S101", AHORA, [reserva("S101", -15)], True),
                         "En uso (reservada)")


class TestRecomendacion(unittest.TestCase):
    def test_elige_la_mas_pequena_que_alcanza(self):
        r = lg.recomendar_salas(SALAS, [], SIN_SENSORES, 3, AHORA, 60, AHORA)
        self.assertEqual(r[0]["id"], "S101")          # 4 puestos para 3 personas

    def test_excluye_sala_con_choque(self):
        r = lg.recomendar_salas(SALAS, [reserva("S101", 30)], SIN_SENSORES, 3, AHORA, 60, AHORA)
        self.assertNotIn("S101", [s["id"] for s in r])

    def test_reservas_contiguas_no_chocan(self):
        r = lg.recomendar_salas(SALAS, [reserva("S101", 60)], SIN_SENSORES, 3, AHORA, 60, AHORA)
        self.assertEqual(r[0]["id"], "S101")          # 10:00-11:00 y 11:00-12:00

    def test_excluye_ocupada_por_sensor_si_es_para_ya(self):
        sensores = {**SIN_SENSORES, "S101": True}
        r = lg.recomendar_salas(SALAS, [], sensores, 3, AHORA, 60, AHORA)
        self.assertEqual(r[0]["id"], "S102")

    def test_sensor_no_importa_si_es_mas_tarde(self):
        sensores = {**SIN_SENSORES, "S101": True}
        r = lg.recomendar_salas(SALAS, [], sensores, 3, AHORA + timedelta(hours=2), 60, AHORA)
        self.assertEqual(r[0]["id"], "S101")

    def test_requisito_pantalla(self):
        r = lg.recomendar_salas(SALAS, [], SIN_SENSORES, 2, AHORA, 60, AHORA, requiere_pantalla=True)
        self.assertTrue(all(s["pantalla"] for s in r))

    def test_sin_opciones(self):
        self.assertEqual(lg.recomendar_salas(SALAS, [], SIN_SENSORES, 10, AHORA, 60, AHORA), [])


class TestNoShow(unittest.TestCase):
    def test_libera_tras_tolerancia(self):
        vig, lib = lg.liberar_no_shows([reserva("S101", -11)], SIN_SENSORES, AHORA)
        self.assertEqual((len(vig), len(lib)), (0, 1))

    def test_no_libera_dentro_de_tolerancia(self):
        vig, lib = lg.liberar_no_shows([reserva("S101", -10)], SIN_SENSORES, AHORA)
        self.assertEqual((len(vig), len(lib)), (1, 0))

    def test_no_libera_si_el_grupo_llego_y_salio_un_momento(self):
        r = reserva("S101", -20)
        lg.liberar_no_shows([r], {**SIN_SENSORES, "S101": True}, AHORA - timedelta(minutes=15))
        vig, lib = lg.liberar_no_shows([r], SIN_SENSORES, AHORA)
        self.assertEqual(len(lib), 0)


if __name__ == "__main__":
    unittest.main()
