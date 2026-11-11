"""evaluar_newton — cuaderno 02.

Libro: ecuación (18.7), evaluada con Horner.
"""

def evaluar_newton(x, coef, xx):
    """Evalúa el polinomio de Newton con los nodos ``x`` y los ``coef``."""
    raise NotImplementedError("Completa evaluar_newton")


if __name__ == "__main__":
    print(evaluar_newton([1, 4, 6], [0, 0.4620981, -0.0518731], 2))
    # esperado: 0.5658444
