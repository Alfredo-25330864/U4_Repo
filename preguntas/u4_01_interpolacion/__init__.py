"""Preguntas del cuaderno ``u4_01_interpolacion``.

Teóricas, de opción múltiple: el código ya se escribe en ``ejercicios/`` y se
comprueba con ``practica(...)``, así que aquí se evalúa el criterio.
"""

from mn_motor.mcq import desde_markdown

_BASE = "preguntas/u4_01_interpolacion/"

PREGUNTAS = [
    desde_markdown(_BASE + "t01_intervalo.md"),
    desde_markdown(_BASE + "t06_pendiente.md"),
    desde_markdown(_BASE + "t02_grado.md"),
    desde_markdown(_BASE + "t05_unicidad.md"),
    desde_markdown(_BASE + "t03_error.md"),
    desde_markdown(_BASE + "t04_extrapolar.md"),
]