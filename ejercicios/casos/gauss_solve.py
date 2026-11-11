"""gauss_solve — caso del cuaderno 04 (repaso de la Unidad 3).

Eliminación gaussiana hacia adelante + sustitución hacia atrás. Es el mismo
método de la Unidad 3; aquí se reutiliza para resolver las ecuaciones normales
de un ajuste.
"""


def gauss_eliminar(A, b):
    """Triangulariza [A|b] hacia adelante. Devuelve la matriz aumentada.

    Sin pivoteo: si aparece un pivote cero, lanza ZeroDivisionError.
    """
    raise NotImplementedError("Completa gauss_eliminar")


def sustitucion_atras(Ab):
    """Despeja x de una matriz aumentada triangular superior.

    Devuelve una lista de números.
    """
    raise NotImplementedError("Completa sustitucion_atras")


def gauss_solve(A, b):
    """Método completo: eliminación + sustitución. Devuelve la lista de x."""
    Ab = gauss_eliminar(A, b)
    raise NotImplementedError("Completa gauss_solve llamando a sustitucion_atras")


if __name__ == "__main__":
    # sistema 2x2: 2x1 + x2 = 4;  x1 + 3x2 = 7   ->   [1.0, 2.0]
    print(gauss_solve([[2, 1], [1, 3]], [4, 7]))
