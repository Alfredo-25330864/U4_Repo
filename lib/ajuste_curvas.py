"""ajuste_curvas — interpolación y ajuste por mínimos cuadrados (Unidad 4).

Funciones puras (sin estado, sin gráficas) para que sirvan igual en un
cuaderno, en un script o en las pruebas. Todas reciben arreglos de NumPy o
listas y devuelven ``float``/``ndarray``/``dict`` explícitos.

Convenciones
------------
* ``x``, ``y``, ``t`` son arreglos 1-D del mismo tamaño.
* Los coeficientes de un polinomio se devuelven en orden **creciente**
  ``[a0, a1, ..., am]`` salvo en Newton, donde son las diferencias divididas
  ``[b0, b1, ..., bn]``.
* ``r2`` es el coeficiente de determinación de la ecuación (17.10) del libro.
"""

from __future__ import annotations

import numpy as np


# ----------------------------------------------------------------------
# Interpolación de Newton en diferencias divididas
# ----------------------------------------------------------------------
def tabla_diferencias(x, y):
    """Tabla triangular de diferencias divididas.

    ``T[i, j]`` es la diferencia de orden ``j`` que termina en ``x[i]``:

    .. math:: T[i,j] = \\frac{T[i,j-1] - T[i-1,j-1]}{x_i - x_{i-j}}

    La diagonal ``np.diag(T)`` son los coeficientes ``b0..bn`` del polinomio
    de Newton, ecuaciones (18.8)-(18.14) del libro.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x y y deben ser arreglos 1-D del mismo tamaño")
    if np.unique(x).size != x.size:
        raise ValueError("las abscisas deben ser distintas")
    n = x.size
    T = np.zeros((n, n))
    T[:, 0] = y
    for j in range(1, n):
        T[j:, j] = (T[j:, j - 1] - T[j - 1:-1, j - 1]) / (x[j:] - x[:-j])
    return T


def coeficientes_newton(x, y):
    """Coeficientes ``b0..bn`` (diagonal de la tabla de diferencias)."""
    return np.diag(tabla_diferencias(x, y))


def evaluar_newton(x, coef, xx):
    """Evalúa el polinomio de Newton con el esquema de Horner.

    ``x`` son las abscisas nodales y ``coef`` los ``b`` de la ecuación (18.7).
    """
    x = np.asarray(x, dtype=float)
    coef = np.asarray(coef, dtype=float)
    xx = np.asarray(xx, dtype=float)
    if coef.size != x.size:
        raise ValueError("se requiere un coeficiente por nodo")
    p = np.full_like(xx, coef[-1], dtype=float)
    for k in range(coef.size - 2, -1, -1):
        p = p * (xx - x[k]) + coef[k]
    return float(p) if p.ndim == 0 else p


def newton(x, y, xx):
    """Atajo: coeficientes + evaluación del polinomio de Newton."""
    return evaluar_newton(x, coeficientes_newton(x, y), xx)


# ----------------------------------------------------------------------
# Interpolación de Lagrange
# ----------------------------------------------------------------------
def evaluar_lagrange(x, y, xx):
    """Polinomio de Lagrange, ecuaciones (18.20) y (18.21).

    Cada peso ``L_i`` vale 1 en ``x_i`` y 0 en los demás nodos; por eso la
    suma reproduce exactamente los datos.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xx = np.atleast_1d(np.asarray(xx, dtype=float))
    if x.size != y.size:
        raise ValueError("x y y deben tener el mismo tamaño")
    total = np.zeros_like(xx)
    for i in range(x.size):
        peso = np.ones_like(xx)
        for j in range(x.size):
            if i != j:
                peso *= (xx - x[j]) / (x[i] - x[j])
        total += peso * y[i]
    return float(total[0]) if total.size == 1 else total


# ----------------------------------------------------------------------
# Regresión por mínimos cuadrados
# ----------------------------------------------------------------------
def _vandermonde(x, grado):
    x = np.asarray(x, dtype=float)
    return np.vander(x, N=grado + 1, increasing=True)


def minimos_cuadrados(x, y, grado=1):
    """Ajuste polinomial por mínimos cuadrados de grado ``m``.

    Resuelve las ecuaciones normales (17.4)-(17.5) para ``m = 1`` y
    (17.19) para ``m = 2``, generalizadas a cualquier grado. Devuelve un
    diccionario con:

    ``coef`` (a0..am), ``pred``, ``residuales``, ``Sr``, ``St``, ``r2``,
    ``syx`` (error estándar, ecuación 17.20) y ``grados_libertad``.
    Si el número de coeficientes iguala al de datos, ``grados_libertad`` es 0
    y ``syx`` es ``inf``: el modelo interpola y no permite estimar el error.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if grado < 0:
        raise ValueError("el grado debe ser >= 0")
    if x.size != y.size:
        raise ValueError("x y y deben tener el mismo tamaño")
    n = x.size
    if n < grado + 1:
        raise ValueError("se requieren al menos tantos datos como coeficientes")

    V = _vandermonde(x, grado)
    # Ecuaciones normales: (V^T V) a = V^T y
    coef = np.linalg.solve(V.T @ V, V.T @ y)
    pred = V @ coef
    residuales = y - pred
    Sr = float(np.sum(residuales ** 2))
    St = float(np.sum((y - np.mean(y)) ** 2))
    gl = n - (grado + 1)
    return {
        "coef": coef,
        "pred": pred,
        "residuales": residuales,
        "Sr": Sr,
        "St": St,
        "r2": float((St - Sr) / St) if St > 0 else float("nan"),
        "syx": float(np.sqrt(Sr / gl)) if gl > 0 else float("inf"),
        "grados_libertad": gl,
    }


def evaluar_polinomio(coef, xx):
    """Evalúa ``a0 + a1 x + ... + am x^m`` (coeficientes crecientes)."""
    return np.polynomial.polynomial.polyval(np.asarray(xx, dtype=float),
                                            np.asarray(coef, dtype=float))


# ----------------------------------------------------------------------
# Ajuste con funciones sinusoidales (sección 19.1)
# ----------------------------------------------------------------------
def ajuste_sinusoidal(t, y, omega0):
    """Mínimos cuadrados para ``y = A0 + A1 cos(w t) + B1 sen(w t)``.

    Ecuaciones (19.11)-(19.12). Devuelve ``A0``, ``A1``, ``B1``, la amplitud
    ``C1`` (19.9), la fase ``theta`` (19.8) y la suma de residuos ``Sr``.
    """
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    if t.size != y.size:
        raise ValueError("t y y deben tener el mismo tamaño")
    V = np.column_stack([np.ones_like(t), np.cos(omega0 * t), np.sin(omega0 * t)])
    coef = np.linalg.solve(V.T @ V, V.T @ y)
    A0, A1, B1 = (float(c) for c in coef)
    pred = V @ coef
    return {
        "A0": A0,
        "A1": A1,
        "B1": B1,
        "C1": float(np.hypot(A1, B1)),
        "theta": float(np.arctan2(-B1, A1)),
        "promedio_omega0": omega0,
        "Sr": float(np.sum((y - pred) ** 2)),
        "pred": pred,
    }


def coeficientes_fourier(t, y, omega0, m):
    """Coeficientes de Fourier para datos igualmente espaciados.

    Devuelve ``A0``, ``A = [A1..Am]`` y ``B = [B1..Bm]`` con las ecuaciones
    (19.14)-(19.16). ``m`` es el armónico máximo.
    """
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    N = y.size
    A = np.array([2.0 / N * np.sum(y * np.cos(j * omega0 * t))
                  for j in range(1, m + 1)])
    B = np.array([2.0 / N * np.sum(y * np.sin(j * omega0 * t))
                  for j in range(1, m + 1)])
    return {"A0": float(np.sum(y) / N), "A": A, "B": B}


def evaluar_fourier(t, coef, omega0):
    """Evalúa la serie de Fourier truncada en ``m`` armónicos."""
    t = np.asarray(t, dtype=float)
    total = np.full_like(t, coef["A0"], dtype=float)
    for j, (Aj, Bj) in enumerate(zip(coef["A"], coef["B"]), start=1):
        total = total + Aj * np.cos(j * omega0 * t) + Bj * np.sin(j * omega0 * t)
    return total


# ----------------------------------------------------------------------
# Puente con optimización: interpolación parabólica (capítulo 4, 13.2)
# ----------------------------------------------------------------------
def x_parabolico(x0, x1, x2, f0, f1, f2):
    """Abscisa del vértice de la parábola que pasa por tres puntos.

    Es la ecuación (13.7) del capítulo 4, usada para localizar un óptimo.
    """
    num = f0 * (x1 ** 2 - x2 ** 2) + f1 * (x2 ** 2 - x0 ** 2) + f2 * (x0 ** 2 - x1 ** 2)
    den = 2 * f0 * (x1 - x2) + 2 * f1 * (x2 - x0) + 2 * f2 * (x0 - x1)
    if den == 0:
        raise ZeroDivisionError("los tres puntos son colineales: no hay parábola única")
    return num / den


def interpolacion_parabolica(f, x0, x1, x2, tol=1e-6, max_iter=20):
    """Itera la ecuación (13.7) con descarte regionalizado.

    Devuelve ``x_opt``, ``f_opt``, ``iteraciones`` y el ``historial`` de
    triples evaluados. Se conserva el punto de mayor ``f`` y se descarta el
    extremo opuesto, igual que en el ejemplo 13.2 del libro.
    """
    puntos = [(float(x0), float(f(x0))), (float(x1), float(f(x1))),
              (float(x2), float(f(x2)))]
    historial = []
    for _ in range(max_iter):
        (a, fa), (b, fb), (c, fc) = puntos
        nuevo = x_parabolico(a, b, c, fa, fb, fc)
        fn = float(f(nuevo))
        historial.append((nuevo, fn))
        if abs(nuevo - b) < tol:
            break
        # regionalización: el mejor punto queda al centro de la terna
        if fn > fb:
            if nuevo > b:
                puntos = [(b, fb), (nuevo, fn), (c, fc)]
            else:
                puntos = [(a, fa), (nuevo, fn), (b, fb)]
        else:
            if nuevo > b:
                puntos = [(a, fa), (b, fb), (nuevo, fn)]
            else:
                puntos = [(nuevo, fn), (b, fb), (c, fc)]
    mejor = max(historial, key=lambda p: p[1])
    return {"x_opt": mejor[0], "f_opt": mejor[1],
            "iteraciones": len(historial), "historial": historial}


__all__ = [
    "tabla_diferencias", "coeficientes_newton", "evaluar_newton", "newton",
    "evaluar_lagrange", "minimos_cuadrados", "evaluar_polinomio",
    "ajuste_sinusoidal", "coeficientes_fourier", "evaluar_fourier",
    "x_parabolico", "interpolacion_parabolica",
]
