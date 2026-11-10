"""error_estandar — cuaderno 03.

Libro: ecuaciones (17.9) y (17.20).  sy/x = sqrt(Sr / (n - (m + 1)))
"""

def error_estandar(Sr, n, m):
    """Error estándar de la estimación (``m`` es el grado del modelo)."""
    raise NotImplementedError("Completa error_estandar")


if __name__ == "__main__":
    print(error_estandar(3.74657, 6, 2))
    # esperado: 1.1175
