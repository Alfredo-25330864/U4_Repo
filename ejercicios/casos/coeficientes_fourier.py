"""coeficientes_fourier — tarea extra del cuaderno 04.

Libro: ecuaciones (19.14) a (19.16). Devuelve ``(A0, [A1..Am], [B1..Bm])``.
"""

import math


def coeficientes_fourier(t, y, omega0, m):
    """Coeficientes de la serie de Fourier truncada en ``m`` armónicos.

    A0 = sum(y) / N
    Aj = 2/N * sum(y_i cos(j*omega0*t_i))
    Bj = 2/N * sum(y_i sin(j*omega0*t_i))
    """
    raise NotImplementedError("Completa coeficientes_fourier")


if __name__ == "__main__":
    N = 8
    w = 2 * math.pi
    t = [k / N for k in range(N)]
    y = [1 + 2 * math.cos(w * ti) + 3 * math.sin(w * ti) for ti in t]
    print(coeficientes_fourier(t, y, w, 1))
    # esperado: (1.0, [2.0], [3.0])
