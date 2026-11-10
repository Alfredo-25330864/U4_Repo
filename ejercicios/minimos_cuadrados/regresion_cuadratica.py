"""regresion_cuadratica — cuaderno 03.

Libro: ecuación (17.19). Resuelve el sistema 3x3 de las ecuaciones normales.
Devuelve ``[a0, a1, a2]``.
"""

from ejercicios.minimos_cuadrados.suma_residuos_cuadrados import (
    suma_residuos_cuadrados,
)


def regresion_cuadratica(x, y):
    """Ajusta y = a0 + a1 x + a2 x^2 por mínimos cuadrados."""
    raise NotImplementedError("Completa regresion_cuadratica")


if __name__ == "__main__":
    print(regresion_cuadratica(list(range(6)),
                               [2.1, 7.7, 13.6, 27.2, 40.9, 61.1]))
    # esperado: [2.47857, 2.35929, 1.86071]
