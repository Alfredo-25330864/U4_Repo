"""Preguntas del cuaderno `u4_03_minimos_cuadrados`.

Teóricas, de opción múltiple: el código ya se escribe en ``ejercicios/`` y se
comprueba con ``practica(...)``, así que aquí se evalúa el criterio.
"""

from mn_motor.mcq import desde_markdown

_BASE = "preguntas/u4_03_minimos_cuadrados/"

PREGUNTAS = [
    desde_markdown(_BASE + "t01_residuos.md"),
    desde_markdown(_BASE + "t02_ecuaciones_normales.md"),
    desde_markdown(_BASE + "t03_grado.md"),
    desde_markdown(_BASE + "t04_error_estandar.md"),
    desde_markdown(_BASE + "t05_coef_determinacion.md"),
]