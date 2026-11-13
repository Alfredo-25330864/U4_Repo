"""Preguntas del cuaderno `u4_02_newton_lagrange`.

Teóricas, de opción múltiple: el código ya se escribe en ``ejercicios/`` y se
comprueba con ``practica(...)``, así que aquí se evalúa el criterio.
"""

from mn_motor.mcq import desde_markdown

_BASE = "preguntas/u4_02_newton_lagrange/"

PREGUNTAS = [
    desde_markdown(_BASE + "t01_diferencias.md"),
    desde_markdown(_BASE + "t02_agregar_nodo.md"),
    desde_markdown(_BASE + "t03_lagrange.md"),
    desde_markdown(_BASE + "t04_error_nodo_extra.md"),
]