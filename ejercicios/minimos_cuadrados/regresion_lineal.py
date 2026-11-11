"""regresion_lineal — cuaderno 03.

Libro: ecuaciones (17.4) a (17.7). Devuelve ``[a0, a1]``.
"""

from ejercicios.minimos_cuadrados.suma_residuos_cuadrados import (
    suma_residuos_cuadrados,
)


def regresion_lineal(x, y):
    """Ajusta y = a0 + a1 x por mínimos cuadrados."""
    raise NotImplementedError("Completa regresion_lineal")


if __name__ == "__main__":
    print(regresion_lineal([1, 2, 3, 4, 5, 6, 7],
                           [0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5]))
    # esperado: [0.0714286, 0.8392857]
