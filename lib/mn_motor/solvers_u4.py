"""solvers_u4 — implementaciones de REFERENCIA para la Unidad 4.

Viven en el motor, nunca en el cuaderno: son contra lo que se comparan las
funciones que escriben los alumnos. Se escriben con aritmética exacta (sympy)
siempre que se pueda, para que la comparación no dependa de tolerancias ni
confunda un error de redondeo con un error de método.

Un método completo y sus piezas sueltas son funciones distintas, igual que en
el cuaderno: la función del método LLAMA a las de sus pasos, así el alumno
puede probar cada pieza por separado.
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


# ======================================================================
# 4.1 — Interpolación lineal y cuadrática
# ======================================================================
def interpolacion_lineal(x0, f0, x1, f1, x):
    """Ecuación (18.2): recta que pasa por dos nodos, evaluada en ``x``."""
    x0, f0, x1, f1, x = map(_racional, (x0, f0, x1, f1, x))
    if x1 == x0:
        raise ZeroDivisionError('los dos nodos deben ser distintos')
    return sp.nsimplify(f0 + (f1 - f0) / (x1 - x0) * (x - x0))


def coeficientes_cuadraticos(x0, f0, x1, f1, x2, f2):
    """``[b0, b1, b2]`` de la parábola (18.3), con (18.4)–(18.6)."""
    x0, f0, x1, f1, x2, f2 = map(_racional, (x0, f0, x1, f1, x2, f2))
    if x0 == x1 or x1 == x2 or x0 == x2:
        raise ZeroDivisionError('los tres nodos deben ser distintos')
    b0 = f0
    b1 = sp.nsimplify((f1 - f0) / (x1 - x0))
    pend2 = (f2 - f1) / (x2 - x1)
    b2 = sp.nsimplify((pend2 - b1) / (x2 - x0))
    return [sp.nsimplify(b0), b1, b2]


def interpolacion_cuadratica(x0, f0, x1, f1, x2, f2, x):
    """Parábola por tres nodos en forma anidada (18.3).

    Llama a ``coeficientes_cuadraticos``: la pieza suelta y el método completo
    no se programan dos veces.
    """
    b0, b1, b2 = coeficientes_cuadraticos(x0, f0, x1, f1, x2, f2)
    x0, x1, x = _racional(x0), _racional(x1), _racional(x)
    return sp.nsimplify(b0 + b1 * (x - x0) + b2 * (x - x0) * (x - x1))


def error_estimado_interpolacion(dif_siguiente, nodos, x):
    """Estimación del error con un punto extra, ecuación (18.18).

    ``Rn = f[x_{n+1},...,x_0] * prod(x - x_i)``.
    """
    producto = sp.Integer(1)
    for xi in nodos:
        producto *= (_racional(x) - _racional(xi))
    return sp.nsimplify(_racional(dif_siguiente) * producto)


# ======================================================================
# 4.2 — Newton en diferencias divididas y Lagrange
# ======================================================================
def tabla_diferencias(x, y):
    """Tabla triangular completa de diferencias divididas, (18.12)–(18.14).

    ``T[i][j]`` es la diferencia de orden ``j`` que termina en ``x[i]``; las
    casillas que no se usan quedan en 0 para que la tabla sea rectangular.
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
    return T


def coeficientes_newton(x, y):
    """``b0..bn``: la diagonal de la tabla, ecuaciones (18.8)–(18.11)."""
    T = tabla_diferencias(x, y)
    return [T[i][i] for i in range(len(T))]


def evaluar_newton(x, coef, xx):
    """Evalúa la forma (18.7) con Horner."""
    xv = _vector(x)
    b = _vector(coef)
    if len(b) != len(xv):
        raise ValueError('se requiere un coeficiente por nodo')
    p = b[-1]
    for k in range(len(b) - 2, -1, -1):
        p = sp.nsimplify(p * (_racional(xx) - xv[k]) + b[k])
    return sp.nsimplify(p)


def interpolacion_newton(x, y, xx):
    """Método completo: coeficientes + evaluación."""
    return evaluar_newton(x, coeficientes_newton(x, y), xx)


def interpolacion_lagrange(x, y, xx):
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


def error_newton(x, coef, xx):
    """Término de grado ``n`` como estimación del error, ecuación (18.19).

    Es ``b_n * prod_{i<n}(x - x_i)``: la diferencia entre las predicciones de
    grado ``n`` y ``n+1``.
    """
    xv = _vector(x)
    b = _vector(coef)
    if len(b) != len(xv):
        raise ValueError('se requiere un coeficiente por nodo')
    producto = sp.Integer(1)
    for xi in xv[:-1]:
        producto *= (_racional(xx) - xi)
    return sp.nsimplify(b[-1] * producto)


# ======================================================================
# 4.3 — Mínimos cuadrados
# ======================================================================
def suma_residuos_cuadrados(x, y, coef):
    """``Sr`` de la ecuación (17.3), para coeficientes crecientes."""
    xv, yv = _vector(x), _vector(y)
    a = _vector(coef)
    total = sp.Integer(0)
    for xi, yi in zip(xv, yv):
        modelo = sum(aj * xi ** j for j, aj in enumerate(a))
        total += (yi - modelo) ** 2
    return sp.nsimplify(total)


def _normal(xv, yv, m):
    """Resuelve las ecuaciones normales (17.19) y devuelve ``a0..am``."""
    V = sp.Matrix([[xi ** j for j in range(m + 1)] for xi in xv])
    rhs = sp.Matrix(yv)
    coef = (V.T * V).LUsolve(V.T * rhs)
    return [sp.nsimplify(v) for v in coef]


def sistema_normal(x, y, grado):
    """``(A, b)`` de las ecuaciones normales, para resolverlas por Gauss.

    Es el puente entre las dos unidades: el ajuste produce un sistema lineal
    y la eliminación gaussiana lo resuelve.
    """
    xv, yv = _vector(x), _vector(y)
    m = int(grado)
    if len(xv) != len(yv):
        raise ValueError('x y y deben tener el mismo tamaño')
    if len(xv) < m + 1:
        raise ValueError('se requieren al menos tantos datos como coeficientes')
    A = [[sum(xi ** (i + j) for xi in xv) for j in range(m + 1)]
         for i in range(m + 1)]
    b = [sum(yi * xi ** i for xi, yi in zip(xv, yv)) for i in range(m + 1)]
    return [[float(v) for v in fila] for fila in A], [float(v) for v in b]


def coeficientes_calibracion(x, y, grado=1):
    """Ajuste por mínimos cuadrados resuelto con **eliminación gaussiana**.

    Combina la Unidad 4 (ecuaciones normales) con la Unidad 3 (sistema lineal):
    arma ``A a = b`` y lo resuelve con ``solvers_u3.gauss_solve``.
    """
    import mn_motor.solvers_u3 as u3

    A, b = sistema_normal(x, y, grado)
    return u3.gauss_solve(A, b)


def regresion_lineal(x, y):
    """``[a0, a1]`` con las ecuaciones normales (17.4)–(17.7)."""
    xv, yv = _vector(x), _vector(y)
    if len(xv) != len(yv):
        raise ValueError('x y y deben tener el mismo tamaño')
    if len(xv) < 2:
        raise ValueError('se necesitan al menos 2 datos')
    return _normal(xv, yv, 1)


def regresion_cuadratica(x, y):
    """``[a0, a1, a2]`` con las ecuaciones normales (17.19)."""
    xv, yv = _vector(x), _vector(y)
    if len(xv) != len(yv):
        raise ValueError('x y y deben tener el mismo tamaño')
    if len(xv) < 3:
        raise ValueError('se necesitan al menos 3 datos')
    return _normal(xv, yv, 2)


def suma_cuadrados_total(y):
    """``St``: suma de cuadrados alrededor de la media."""
    yv = _vector(y)
    if not yv:
        raise ValueError('no hay datos')
    media = sp.nsimplify(sum(yv) / len(yv))
    return sp.nsimplify(sum((yi - media) ** 2 for yi in yv))


def error_estandar(Sr, n, m):
    """``sy/x`` de las ecuaciones (17.9) y (17.20)."""
    Sr, n, m = _racional(Sr), int(n), int(m)
    gl = n - (m + 1)
    if gl <= 0:
        raise ValueError('no quedan grados de libertad para estimar el error')
    return sp.nsimplify(sp.sqrt(Sr / gl))


def coeficiente_determinacion(Sr, St):
    """``r^2`` de la ecuación (17.10)."""
    Sr, St = _racional(Sr), _racional(St)
    if St == 0:
        raise ValueError('St = 0: los datos no tienen dispersión')
    return sp.nsimplify((St - Sr) / St)


# ======================================================================
# Tarea extra — Fourier (sección 19.1)
# ======================================================================
def coeficientes_fourier(t, y, omega0, m):
    """``(A0, A, B)`` con las ecuaciones (19.14)–(19.16).

    Aquí NO se usa aritmética exacta: los coeficientes de Fourier se evalúan
    con ``cos`` y ``sin``, y racionalizar ``omega0`` cambiaría el resultado.
    """
    import math

    tv = [float(v) for v in t]
    yv = [float(v) for v in y]
    if len(tv) != len(yv):
        raise ValueError('t y y deben tener el mismo tamaño')
    N = len(tv)
    if N == 0:
        raise ValueError('no hay datos')
    w = float(omega0)
    m = int(m)
    A0 = sum(yv) / N
    A = [2.0 / N * sum(yi * math.cos(j * w * ti) for ti, yi in zip(tv, yv))
         for j in range(1, m + 1)]
    B = [2.0 / N * sum(yi * math.sin(j * w * ti) for ti, yi in zip(tv, yv))
         for j in range(1, m + 1)]
    return A0, A, B


def evaluar_fourier(t, coef, omega0):
    """Evalúa ``A0 + sum(Aj cos(j w t) + Bj sin(j w t))``."""
    import math

    A0, A, B = coef
    w = float(omega0)
    salida = []
    for ti in [float(v) for v in t]:
        total = float(A0)
        for j, (Aj, Bj) in enumerate(zip(A, B), start=1):
            total += float(Aj) * math.cos(j * w * ti)
            total += float(Bj) * math.sin(j * w * ti)
        salida.append(total)
    return salida


# ======================================================================
# Puente con optimización (capítulo 4, sección 13.2)
# ======================================================================
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
    'coeficiente_determinacion',
    'coeficientes_calibracion',
    'coeficientes_cuadraticos',
    'coeficientes_fourier',
    'coeficientes_newton',
    'error_estandar',
    'error_estimado_interpolacion',
    'error_newton',
    'evaluar_fourier',
    'evaluar_newton',
    'interpolacion_cuadratica',
    'interpolacion_lagrange',
    'interpolacion_lineal',
    'interpolacion_newton',
    'regresion_cuadratica',
    'regresion_lineal',
    'sistema_normal',
    'suma_cuadrados_total',
    'suma_residuos_cuadrados',
    'tabla_diferencias',
    'x_parabolico',
]
