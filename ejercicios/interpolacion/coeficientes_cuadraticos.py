"""coeficientes_cuadraticos — cuaderno 01.

Libro: ecuaciones (18.4), (18.5) y (18.6). Devuelve ``[b0, b1, b2]``.
"""

def coeficientes_cuadraticos(x0, y0, x1, y1, x2, y2):
    """Devuelve [b0, b1, b2] de f2(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1)."""
    b0 = float(y0)

    m1 = (y1 - y0) / (x1 - x0)
    m2 = (y2 - y1) / (x2 - x1)

    b1 = m1
    b2 = (m2 - m1) / (x2 - x0)

    y = b0 + b1 * (x2 - x0) + b2 * (x2 - x0) * (x2 - x1)

    return [b0, b1, b2]

    raise NotImplementedError("Completa coeficientes_cuadraticos")


if __name__ == "__main__":
    # nodos (0,1), (1,3), (2,7)  ->  [1.0, 2.0, 1.0]
    print(coeficientes_cuadraticos(0, 1, 1, 3, 2, 7))
