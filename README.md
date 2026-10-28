# MVP – Salas de estudio Ad Portas
**Grupo 2 · Introducción a los Sistemas Inteligentes · Universidad de La Sabana · Tercer corte**

Aplicación web en Python + Streamlit que muestra qué salas de estudio de Ad Portas están libres **en este momento** (combinando sensor de presencia + reservas) y recomienda/reserva la sala que mejor se ajusta a un grupo.

> ⚠️ Los campos marcados con **[COMPLETAR]** dependen de datos que solo tiene el equipo (resultados de encuestas, número real de salas, horarios). Reemplácenlos antes de entregar.

---

## 1. Ficha del proyecto (sección 1.1 de la guía)

| Elemento | Respuesta del equipo |
|---|---|
| **Problema** | Los estudiantes van hasta Ad Portas sin saber si hay salas libres; además hay salas reservadas que nadie usa (no-shows) y salas grandes ocupadas por 1 o 2 personas. |
| **Usuario** | Estudiantes de pregrado de La Sabana que estudian en grupo entre clases. Secundario: personal administrativo de Ad Portas que gestiona las salas. |
| **Evidencia** | Encuesta/observación de los cortes 1 y 2: **[COMPLETAR: n.º de encuestados, % que no encontró sala, tiempo promedio buscando, observación de salas reservadas vacías]**. |
| **Decisión o tarea** | Saber si vale la pena ir a Ad Portas y reservar en menos de 1 minuto la sala adecuada para su grupo. |
| **Datos** | Lista de salas (capacidad, piso, tablero, pantalla) → Ad Portas; presencia por sala → sensor (simulado en el MVP); reservas → la propia app. |
| **Éxito** | Que el usuario complete una reserva sin ayuda en < 60 s y que interprete correctamente el estado de las salas. |

## 2. Propuesta de valor (mini ejercicio 1)

> Para **estudiantes de La Sabana** que necesitan **un espacio para estudiar en grupo**, el MVP permite **ver en tiempo real qué salas de Ad Portas están libres y reservar la más adecuada** para conseguir **encontrar sala en menos de un minuto sin desplazarse en vano**.

## 3. Alcance del MVP (sección 1.2)

- **Debe tener (incluido):** ver disponibilidad actual, formulario de búsqueda con validaciones, recomendación de sala, confirmar y cancelar reserva, liberación automática de no-shows.
- **Podría tener (no incluido):** reservas para otros días, historial, notificaciones, mapa del edificio, estadísticas de ocupación.
- **No requiere en esta fase:** login con correo institucional, sensores físicos reales, pagos, integración con sistemas de la universidad.

## 4. Flujo (mini ejercicio 2)

```
Usuario ──► Entrada ──────────────────► Procesamiento ─────────────────────► Respuesta
            (personas, hora, duración,   [R1] estado = sensor + reservas      Estado por sala (🟢🟡🔴🟠)
             tablero/pantalla, alias)    [R2] filtrar y ordenar salas  ◄─ DECISIÓN   Sala sugerida + motivo
                                         [R3] liberar no-shows         ◄─ DECISIÓN   Reserva confirmada
             └─ solo interfaz ─┘         └── reglas basadas en datos ──┘      └─ solo interfaz ─┘
```

## 5. ¿Dónde está la "inteligencia"? (sección 2 y 5.2)

El MVP **no usa un modelo generativo ni predictivo**: usa **reglas explicables** sobre dos fuentes de datos (sensor + reservas). Se eligió así porque aún no hay datos históricos reales de ocupación para entrenar un modelo, y la guía pide no simular predicciones sin datos.

| Regla | Qué decide | Fundamento |
|---|---|---|
| **R1 – Estado** | Libre / Ocupada sin reserva / En uso / Reservada esperando / No-show | Ni el sensor ni las reservas solos bastan: una sala puede estar reservada y vacía, o ocupada sin reserva. |
| **R2 – Recomendación** | Qué sala sugerir | Menor capacidad que alcance → las salas grandes quedan libres para grupos grandes. Si es para ya, el sensor debe confirmar que está vacía. |
| **R3 – No-show** | Liberar reservas no usadas | Si pasan 10 min desde el inicio y el sensor nunca detectó a nadie, la sala vuelve a estar disponible. |

**Caso donde se equivoca:** si el sensor falla (p. ej. no detecta a alguien quieto leyendo), R3 puede liberar una sala que sí se estaba usando. Mitigación futura: sensores de mayor fiabilidad, botón "Ya llegué" (check-in), o exigir que el sensor marque vacío durante varios minutos seguidos.

**Siguiente paso de IA (fuera del MVP):** con datos de ocupación de varias semanas, entrenar un modelo que prediga la ocupación por franja horaria ("a las 2 p. m. suele haber 1 sala libre").

## 6. Entradas, procesamiento, salida, excepciones, privacidad (sección 5.1)

| | Detalle |
|---|---|
| **Entradas** | Alias (texto, 1–40 caracteres) · personas (entero 1–8) · hora de inicio (hoy, 7:00–21:00) · duración (30/60/90/120 min) · tablero/pantalla (sí/no). Salas desde `data/salas.csv`; sensores desde el panel de pruebas. |
| **Procesamiento** | Reglas R1, R2 y R3 en `logica.py`. |
| **Salida** | Tablero de estados por piso, sala sugerida con explicación, confirmación de reserva. |
| **Excepciones** | Alias vacío, grupo más grande que cualquier sala, hora pasada, reserva que termina después del cierre, sin salas disponibles, doble reserva simultánea (se relee el archivo antes de confirmar), archivo de reservas dañado. |
| **Privacidad** | No se pide nombre real, cédula, código ni teléfono: solo un alias. El sensor detecta **presencia (sí/no)**, no identifica personas ni graba imagen. Las reservas se guardan solo en `data/reservas.json` en el equipo que ejecuta la app. |

## 7. Historias de usuario (mini ejercicio 5)

1. **Como** estudiante que sale de clase, **quiero** ver qué salas están libres ahora **para** no caminar hasta Ad Portas en vano.
   *Criterio:* al abrir la app se muestra cuántas salas están libres y el estado de cada una con color + texto.
2. **Como** estudiante que coordina un grupo de 3, **quiero** que la app me sugiera una sala adecuada **para** no reservar una sala de 8 innecesariamente.
   *Criterio:* con 3 personas y todas las salas libres, la sugerencia es una sala de 4 puestos.
3. **Como** estudiante que no encuentra sala, **quiero** que las reservas no usadas se liberen **para** poder usar esas salas.
   *Criterio:* una reserva con 11 minutos de iniciada y sin presencia desaparece y la sala aparece libre.

## 8. Estructura

```
mvp-salas-adportas/
├── app.py              # interfaz Streamlit
├── logica.py           # reglas R1, R2, R3 (sin Streamlit, se pueden probar)
├── test_logica.py      # 21 pruebas automáticas
├── data/salas.csv      # salas (ILUSTRATIVAS – reemplazar por las reales)
├── requirements.txt
├── README.md · pruebas.md · adopcion.md · registro_ia.md
└── evidencias/         # capturas de pantalla y notas de pruebas con usuarios
```

## 9. Instalación y ejecución

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell  (cmd: .venv\Scripts\activate.bat)
source .venv/bin/activate             # macOS / Linux
python -m pip install -r requirements.txt
python -m streamlit run app.py
python -m unittest -v                 # pruebas automáticas de las reglas
```

**Para la demo en clase:** en la barra lateral, activar "Usar hora manual" y marcar/desmarcar los sensores para mostrar cómo cambia el estado de las salas y cómo se libera un no-show.

## 10. Limitaciones conocidas

- Los sensores y la lista de salas son **simulados**; el número real de salas y sus características deben tomarse de Ad Portas **[COMPLETAR]**.
- Sin login: cualquiera puede cancelar cualquier reserva (aceptable para un piloto, no para producción).
- Las reservas se guardan en un archivo JSON local; si se despliega en Streamlit Community Cloud, se pueden perder cuando la app se reinicia. Para producción haría falta una base de datos.
- Solo reservas para el día actual.
