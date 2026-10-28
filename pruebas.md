# Pruebas del MVP – Salas Ad Portas (sección 7 de la guía)

## 7.1 Matriz de pruebas manuales (en la app)

Preparación: activar **"Usar hora manual"** en la barra lateral y fijar 10:00 a. m. Todos los sensores sin marcar.

| # | Caso | Entrada / acción | Resultado esperado | Resultado obtenido | ¿Cumple? |
|---|---|---|---|---|---|
| 1 | Normal | Alias "Grupo 2", 3 personas, 10:05, 60 min → Buscar → Confirmar | Sugiere una sala de 4 puestos y la reserva aparece en "Reservas de hoy" | Por llenar | Por llenar |
| 2 | Normal | Abrir "Disponibilidad ahora" sin reservas ni sensores | "6 de 6" salas libres, todas 🟢 | Por llenar | Por llenar |
| 3 | Límite | 2 personas, 8:00 p. m., 60 min (termina justo a las 9:00 p. m.) | Se acepta | Por llenar | Por llenar |
| 4 | Límite | 8 personas (capacidad máxima) | Solo sugiere la sala de 8 | Por llenar | Por llenar |
| 5 | Erróneo | Alias vacío | Mensaje "Escribe un nombre o alias…" | Por llenar | Por llenar |
| 6 | Erróneo | 10 personas | Mensaje "Ninguna sala admite 10 personas… Divide el grupo" | Por llenar | Por llenar |
| 7 | Erróneo | Hora de inicio 8:00 a. m. (ya pasó) | Mensaje "La hora de inicio ya pasó" | Por llenar | Por llenar |
| 8 | Erróneo | 8:30 p. m. con 60 min | Mensaje sobre horario 7:00–21:00 | Por llenar | Por llenar |
| 9 | Sensor | Marcar presencia en la sala sugerida en el caso 1 y buscar de nuevo para ya | Esa sala ya no se sugiere | Por llenar | Por llenar |
| 10 | Flujo | Reservar sala a las 10:00; cambiar hora manual a 10:05 sin sensor | Sala 🟡 "Reservada (esperando llegada)" | Por llenar | Por llenar |
| 11 | No-show | Misma reserva; cambiar hora a 10:15 sin sensor | Aviso de liberación y la sala vuelve a 🟢 | Por llenar | Por llenar |
| 12 | Llegada | Reservar a las 10:00; a las 10:05 marcar sensor; a las 10:15 desmarcar | La reserva **no** se libera (el grupo ya llegó) | Por llenar | Por llenar |
| 13 | Sin opciones | Pedir pantalla + 8 personas cuando la sala de 8 está reservada | Mensaje "No hay salas que cumplan…" con sugerencias | Por llenar | Por llenar |
| 14 | Recuperación | Cancelar la reserva en "Reservas de hoy" | Desaparece y la sala vuelve a 🟢 | Por llenar | Por llenar |
| 15 | Concurrencia | Abrir la app en 2 pestañas y reservar la misma sala/hora en ambas | La segunda recibe "Alguien acaba de reservar esa sala" | Por llenar | Por llenar |

> Guardar una captura de pantalla de cada caso en `evidencias/` (ej. `caso_06_grupo_grande.png`).

## Pruebas automáticas de las reglas

`python -m unittest -v` ejecuta 21 pruebas sobre `logica.py` (validación, estados, recomendación, no-shows). **Estado actual: 21/21 pasan.**

## Pruebas con usuarios (mínimo 3 del perfil objetivo)

Tarea que se le da al usuario, **sin explicación verbal** (mini ejercicio 6): *"Eres 3 amigos y quieren estudiar ahora durante una hora con tablero. Usa la app para conseguir sala."*

| Usuario (sin nombre) | Semestre / carrera | ¿Completó? | Tiempo (s) | ¿Explicó bien el estado de las salas? | Dónde se detuvo / comentario | Cambio hecho |
|---|---|---|---|---|---|---|
| U1 | | | | | | |
| U2 | | | | | | |
| U3 | | | | | | |

Preguntas al final: (1) ¿Qué significa el color amarillo? (2) ¿Por qué crees que te sugirió esa sala? (3) Del 1 al 5, ¿qué tan fácil fue? (4) ¿La usarías antes de ir a Ad Portas?

## 7.2 Indicadores y metas (mini ejercicio 7)

| Indicador | Cálculo | Meta | Si no se alcanza… |
|---|---|---|---|
| **Finalización** | usuarios que reservan / usuarios que lo intentan | ≥ 80 % (al menos 3 de 4 o 4 de 5) | Revisar en qué campo se detienen y simplificar el formulario (p. ej. hora "Ahora" por defecto). |
| **Tiempo** | segundos desde abrir la app hasta confirmar | ≤ 60 s en promedio | Mover el botón "Reservar" a la vista de disponibilidad (reservar con un clic desde la sala libre). |
| **Comprensión** | usuarios que explican bien el color 🟡 / consultados | ≥ 80 % | Cambiar el texto del estado y agregar la leyenda arriba en vez de abajo. |
| **Satisfacción** | promedio de facilidad (1–5) | ≥ 4 | Preguntar qué fue lo más difícil y priorizar ese cambio. |
