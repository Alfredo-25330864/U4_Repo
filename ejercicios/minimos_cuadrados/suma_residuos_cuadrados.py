"""suma_residuos_cuadrados — cuaderno 03.

Libro: ecuación (17.3). ``coef`` va en orden CRECIENTE: a0, a1, a2, ...
"""

def suma_residuos_cuadrados(x, y, coef):
    """Devuelve Sr = suma de (y_i - modelo(x_i))^2."""
    raise NotImplementedError("Completa suma_residuos_cuadrados")


if __name__ == "__main__":
    # datos y = 1 + 2x, modelo 1.5 + 1.75x  ->  0.875
    print(suma_residuos_cuadrados([1, 2, 3], [3, 5, 7], [1.5, 1.75]))
