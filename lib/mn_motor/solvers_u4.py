"""solvers_u4 — implementaciones de REFERENCIA para la Unidad 4.

Estas funciones viven en el motor, nunca en el cuaderno: son contra lo que se
comparan las respuestas de los alumnos. Se escriben con aritmética exacta
(sympy) siempre que se pueda, para que la comparación no dependa de tolerancias
ni confunda un error de redondeo con un error de método.

La API es independiente de ``lib/ajuste_curvas.py`` a propósito: el motor debe
poder empaquetarse en el blob sin arrastrar la biblioteca del cuaderno.
"""
from __future__ import annotations

import sympy as sp


def _racional(valor):
    """Convierte int/float/str/Rational de sympy en una expresión exacta."""
    if isinstance(valor, sp.Basic):
        return sp.nsimplify(valor)
    return sp.nsimplify(valor)


def _vector(valores):
    return [_racional(v) for v in valores]


# ----------------------------------------------------------------------
# Interpolación de Newton
# ----------------------------------------------------------------------
def diferencias_divididas(x, y):
    """Coeficientes ``b0..bn`` (diagonal de la tabla de diferencias).

    Ecuaciones (18.8)–(18.14). Falla si hay abscisas repetidas.
    """
    xv, yv = _vector(x), _vector(y)
    if len(xv) != len(yv):
        raise ValueError('x y y deben tener el mismo tamaño')
    if len(set(xv)) != len(xv):
        raise ValueError('las abscisas deben ser distintas')

    n = len(xv)
    T = [[sp.Integer(0)] * n for _ in range(n)]
    for i in range(n):
        T[i][0] = yv[i]
    for j in range(1, n):
        for i in range(j, n):
            T[i][j] = sp.nsimplify(
                (T[i][j - 1] - T[i - 1][j - 1]) / (xv[i] - xv[i - j]))
    return [T[i][i] for i in range(n)]


def evaluar_newton(x, coef, xx):
    """Evalúa la forma (18.7) con Horner, sin diferencias adicionales."""
    xv = _vector(x)
    b = _vector(coef)
    if len(b) != len(xv):
        raise ValueError('se requiere un coeficiente por nodo')
    p = b[-1]
    for k in range(len(b) - 2, -1, -1):
        p = sp.nsimplify(p * (_racional(xx) - xv[k]) + b[k])
    return sp.nsimplify(p)


def newton(x, y, xx):
    """Atajo: diferencias divididas + evaluación en ``xx``."""
    return evaluar_newton(x, diferencias_divididas(x, y), xx)


# ----------------------------------------------------------------------
# Interpolación de Lagrange
# ----------------------------------------------------------------------
def evaluar_lagrange(x, y, xx):
    """Forma de Lagrange, ecuaciones (18.20)–(18.21)."""
    xv, yv = _vector(x), _vector(y)
    if len(xv) != len(yv):
        raise ValueError('x y y deben tener el mismo tamaño')
    if len(set(xv)) != len(xv):
        raise ValueError('las abscisas deben ser distintas')

    xx = _racional(xx)
    total = sp.Integer(0)
    for i in range(len(xv)):
        peso = sp.Integer(1)
        for j in range(len(xv)):
            if i != j:
                peso *= (xx - xv[j]) / (xv[i] - xv[j])
        total += peso * yv[i]
    return sp.nsimplify(total)


# ----------------------------------------------------------------------
# Mínimos cuadrados
# ----------------------------------------------------------------------
def minimos_cuadrados(x, y, grado):
    """Coeficientes ``a0..am`` de las ecuaciones normales (17.19).

    Para ``grado=1`` reproduce (17.4)–(17.7); para ``grado=2``, (17.19).
    Devuelve una lista de coeficientes exactos.
    """
    xv, yv = _vector(x), _vector(y)
    if len(xv) != len(yv):
        raise ValueError('x y y deben tener el mismo tamaño')
    m = int(grado)
    if m < 0:
        raise ValueError('el grado debe ser >= 0')
    if len(xv) < m + 1:
        raise ValueError('se requieren al menos tantos datos como coeficientes')

    V = sp.Matrix([[xi ** j for j in range(m + 1)] for xi in xv])
    rhs = sp.Matrix(yv)
    coef = (V.T * V).LUsolve(V.T * rhs)
    return [sp.nsimplify(v) for v in coef]


def evaluar_polinomio(coef, xx):
    """Evalúa ``a0 + a1 x + ... + am x^m`` (coeficientes crecientes)."""
    xv = _racional(xx)
    total = sp.Integer(0)
    for j, a in enumerate(_vector(coef)):
        total += a * xv ** j
    return sp.nsimplify(total)


# ----------------------------------------------------------------------
# Fourier (sección 19.1)
# ----------------------------------------------------------------------
def coeficientes_fourier(t, y, omega0, m):
    """``(A0, A, B)`` con las ecuaciones (19.14)–(19.16).

    ``A`` y ``B`` son listas de longitud ``m`` (``A1..Am``, ``B1..Bm``).
    Se exige el mismo número de muestras para cada armónico; el llamador es
    responsable de que los datos estén igualmente espaciados.
    """
    tv, yv = _vector(t), _vector(y)
    if len(tv) != len(yv):
        raise ValueError('t y y deben tener el mismo tamaño')
    N = len(tv)
    if N == 0:
        raise ValueError('no hay datos')
    w = _racional(omega0)
    m = int(m)
    A0 = sp.nsimplify(sum(yv) / N)
    A, B = [], []
    for j in range(1, m + 1):
        A.append(sp.nsimplify(2 * sum(yi * sp.cos(j * w * ti)
                                     for ti, yi in zip(tv, yv)) / N))
        B.append(sp.nsimplify(2 * sum(yi * sp.sin(j * w * ti)
                                     for ti, yi in zip(tv, yv)) / N))
    return A0, A, B


def evaluar_fourier(t, coef, omega0):
    """Evalúa ``A0 + sum(Aj cos(j w t) + Bj sin(j w t))``."""
    A0, A, B = coef
    tv = _vector(t)
    w = _racional(omega0)
    salida = []
    for ti in tv:
        total = _racional(A0)
        for j, (Aj, Bj) in enumerate(zip(A, B), start=1):
            total += Aj * sp.cos(j * w * ti) + Bj * sp.sin(j * w * ti)
        salida.append(sp.nsimplify(total))
    return salida


# ----------------------------------------------------------------------
# Puente con optimización (capítulo 4, sección 13.2)
# ----------------------------------------------------------------------
def x_parabolico(x0, x1, x2, f0, f1, f2):
    """Vértice de la parábola por tres puntos, ecuación (13.7)."""
    x0, x1, x2, f0, f1, f2 = map(_racional, (x0, x1, x2, f0, f1, f2))
    num = (f0 * (x1 ** 2 - x2 ** 2) + f1 * (x2 ** 2 - x0 ** 2)
           + f2 * (x0 ** 2 - x1 ** 2))
    den = (2 * f0 * (x1 - x2) + 2 * f1 * (x2 - x0) + 2 * f2 * (x0 - x1))
    if den == 0:
        raise ZeroDivisionError('los tres puntos son colineales')
    return sp.nsimplify(num / den)


__all__ = [
    'coeficientes_fourier',
    'diferencias_divididas',
    'evaluar_fourier',
    'evaluar_lagrange',
    'evaluar_newton',
    'evaluar_polinomio',
    'minimos_cuadrados',
    'newton',
    'x_parabolico',
]
