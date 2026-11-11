"""interpolacion_cuadratica — cuaderno 01.

Libro: ecuación (18.3). Debe LLAMAR a ``coeficientes_cuadraticos``.
"""

from ejercicios.interpolacion.coeficientes_cuadraticos import (
    coeficientes_cuadraticos,
)


def interpolacion_cuadratica(x0, f0, x1, f1, x2, f2, x):
    """Evalúa la parábola por los tres nodos en ``x``."""
    b0, b1, b2 = coeficientes_cuadraticos(x0, f0, x1, f1, x2, f2)
    raise NotImplementedError("Completa interpolacion_cuadratica")


if __name__ == "__main__":
    # mismos nodos, x = 1.5  ->  4.25
    print(interpolacion_cuadratica(0, 1, 1, 3, 2, 7, 1.5))
