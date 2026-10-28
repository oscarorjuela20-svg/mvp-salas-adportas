# Plan de adopción – Salas Ad Portas (sección 9 de la guía)

## 9.1 Actores y resistencias

**Actores:** estudiantes (usuarios finales), personal de Ad Portas / biblioteca (administran las salas), Dirección de Tecnología de la universidad (instalaría los sensores y aprobaría la integración), docentes (podrían recomendar la herramienta).

| Resistencia | Actor | Manifestación observable | Respuesta del equipo | Evidencia de avance |
|---|---|---|---|---|
| **Costumbre** | Estudiantes | "Yo simplemente voy y miro si hay sala" | Piloto de 2 semanas mostrando el tiempo ahorrado; QR en la entrada de Ad Portas y en salones cercanos | % de estudiantes que consultan la app antes de ir |
| **Falta de confianza** | Estudiantes | "La app dice libre y estaba ocupada" | Mostrar por qué cada sala tiene ese estado; botón "Reportar error" | Reportes de error por semana (debe bajar) |
| **Privacidad / vigilancia** | Estudiantes | "¿Me están grabando en la sala?" | Explicar en la app y en un aviso físico que el sensor solo detecta presencia sí/no, sin cámara ni identificación | Aceptación en encuesta; cero quejas formales |
| **Liberación injusta** | Estudiantes | "Me quitaron la sala porque llegué 12 min tarde" | Tolerancia de 10 min visible al reservar; evaluar ampliarla con datos del piloto | Quejas por liberación / no-shows liberados |
| **Pérdida de control** | Personal de Ad Portas | Prefiere el sistema actual de préstamo | Rol de apoyo, no reemplazo: el personal ve el tablero y puede ajustar reservas | Uso del tablero por el personal |
| **Costo e infraestructura** | Dir. de Tecnología | "No hay presupuesto para sensores" | Piloto en 2 salas con sensores de bajo costo; presentar ahorro (no-shows recuperados) | Aprobación del piloto |
| **Falta de acceso** | Estudiantes | Sin datos móviles / mala señal | Pantalla en la entrada de Ad Portas con el mismo tablero | Uso de la pantalla vs. app |

## 9.2 Microplan de adopción

1. **Actor prioritario:** estudiantes que estudian en grupo entre clases, porque son quienes sufren el problema y generan los datos de uso que convencerán a Ad Portas y a Tecnología.
2. **Beneficio demostrable:** saber en segundos si hay sala libre y reservarla sin desplazarse; recuperar salas reservadas que nadie usa.
3. **Resistencia más probable:** **costumbre** ("voy y miro"). Evidencia: **[COMPLETAR con el % de la encuesta que hoy va directamente sin consultar]**.
4. **Acción de mitigación:** piloto de 2 semanas en un piso de Ad Portas, QR visibles en la entrada y en salones cercanos, demostración de 2 minutos en clases del equipo.
5. **Canal de apoyo:** correo/WhatsApp del Grupo 2 y botón de reporte; el personal de Ad Portas recibe dudas presenciales.
6. **Indicador y seguimiento:**
   - Reservas por día y % de reservas con no-show liberado → revisión semanal.
   - Tasa de finalización ≥ 80 % y tiempo ≤ 60 s → medida en pruebas con usuarios al inicio y al final del piloto.
   - Encuesta corta al cierre del piloto (satisfacción ≥ 4/5, intención de seguir usándola).
