"""coeficientes_calibracion — caso del cuaderno 04 (Unidad 3 + Unidad 4).

Un ajuste por mínimos cuadrados produce un **sistema lineal** (las ecuaciones
normales). Aquí se arma ese sistema y se resuelve con eliminación gaussiana:
las dos unidades en una sola función.
"""

from ejercicios.casos.gauss_solve import gauss_solve


def sistema_normal(x, y, grado):
    """Devuelve (A, b) de las ecuaciones normales (17.19).

    A[i][j] = suma de x^(i+j)      b[i] = suma de y * x^i
    """
    raise NotImplementedError("Completa sistema_normal")


def coeficientes_calibracion(x, y, grado=1):
    """Ajusta un polinomio de ``grado`` resolviendo las normales con Gauss."""
    A, b = sistema_normal(x, y, grado)
    raise NotImplementedError("Completa coeficientes_calibracion con gauss_solve")


if __name__ == "__main__":
    x = [0, 10, 20, 30, 40]
    y = [0.1, 1.1, 2.0, 3.1, 3.9]
    print(coeficientes_calibracion(x, y, 1))
    # esperado: [0.07, 0.0975]  (≈ temperatura = 0.07 + 0.0975·cuentas)
