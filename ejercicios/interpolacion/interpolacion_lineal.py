"""interpolacion_lineal — cuaderno 01.

Libro: ecuación (18.2). Recta por dos nodos, evaluada en ``x``.
"""

def interpolacion_lineal(x0, y0, x1, y1, x):
    """Estima f(x) con la recta que pasa por (x0, f0) y (x1, f1)."""
    m = (y1 - y0) / (x1 - x0)
    y = y0 + m * (x - x0)
    return y
    raise NotImplementedError("Completa interpolacion_lineal")


if __name__ == "__main__":
    # f(1)=0, f(4)=3  ->  f(2) = 1.0
    print(interpolacion_lineal(1, 0, 4, 3, 2))
