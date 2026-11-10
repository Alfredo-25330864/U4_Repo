"""interpolacion_lagrange — cuaderno 02.

Libro: ecuaciones (18.20) y (18.21).
"""

def interpolacion_lagrange(x, y, xx):
    """Evalúa el polinomio de Lagrange en ``xx``."""
    raise NotImplementedError("Completa interpolacion_lagrange")


if __name__ == "__main__":
    print(interpolacion_lagrange([1, 4, 6], [0, 1.386294, 1.791759], 2))
    # esperado: 0.5658444 (el mismo polinomio que Newton)
