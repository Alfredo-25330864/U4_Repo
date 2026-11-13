"""Preguntas del cuaderno `u4_04_casos`.

Casos que combinan la Unidad 3 (sistemas lineales) con la Unidad 4 (ajuste de
curvas), más Fourier como tarea extra. Teóricas, de opción múltiple.
"""

from mn_motor.mcq import desde_markdown

_BASE = "preguntas/u4_04_casos/"

PREGUNTAS = [
    desde_markdown(_BASE + "t01_gauss_normales.md"),
    desde_markdown(_BASE + "t02_interpolar_o_ajustar.md"),
    desde_markdown(_BASE + "t03_fourier.md"),
]