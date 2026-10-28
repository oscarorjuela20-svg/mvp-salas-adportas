# Registro de uso de IA (sección 2.1 de la guía – obligatorio)

| Fecha | Herramienta | Propósito | Solicitud resumida | Respuesta aprovechada | Cambios realizados por el equipo | Comprobación independiente |
|---|---|---|---|---|---|---|
| 2026-10-28 | Claude (Anthropic) | Programar y documentar | Adaptar la guía del MVP al proyecto de salas de estudio de Ad Portas | Estructura del proyecto, `logica.py`, `app.py`, pruebas automáticas, borradores de README, pruebas y adopción | **[COMPLETAR]** | Se ejecutaron las 21 pruebas automáticas; **[COMPLETAR: ejecución en el computador del equipo y pruebas manuales]** |
| | | | | | | |

No se compartieron con la IA datos personales, claves ni respuestas individuales de encuestas.

## Prompt propio (mini ejercicio 3)

> Actúa como tutor de desarrollo web para estudiantes universitarios. Problema: los estudiantes de La Sabana no saben si hay salas de estudio libres en Ad Portas y hay salas reservadas que nadie usa. Usuario: estudiantes de pregrado que estudian en grupo entre clases. Datos disponibles: lista de salas (id, piso, capacidad, tablero, pantalla), presencia por sala (sensor sí/no, simulado) y reservas (sala, inicio, fin, personas). Construiremos un MVP en Python y Streamlit que permita ver qué salas están libres ahora y reservar la más adecuada. Propón primero estructura de archivos y criterios de aceptación; luego genera código simple, comentado y ejecutable, separando las reglas de decisión de la interfaz. Incluye validación de entradas, errores previsibles y pruebas. No inventes datos reales ni prometas precisión de un modelo no evaluado. Explica cómo verificar manualmente el resultado.

## Correcciones del equipo sobre la propuesta de la IA (mínimo 2)

Revisar el código y anotar aquí lo que cambiaron. Puntos que vale la pena revisar:

1. **Horario y salas:** la IA supuso 7:00–21:00 y 6 salas ilustrativas → reemplazar por los datos reales de Ad Portas. **[COMPLETAR]**
2. **Tolerancia de no-show:** la IA usó 10 minutos sin evidencia → ajustar según lo que digan los usuarios. **[COMPLETAR]**
3. **[COMPLETAR: cualquier error encontrado al ejecutar o cambio pedido por los usuarios]**
