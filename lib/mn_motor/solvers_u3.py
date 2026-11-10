"""solvers_u3 — referencias de la Unidad 3 (sistemas lineales) para los casos.

El cuaderno 04 combina las dos unidades: las **ecuaciones normales** de un
ajuste son un sistema lineal, y se resuelven con eliminación gaussiana. Estas
son las implementaciones de referencia contra las que se comparan las
funciones del alumno.

Todo en aritmética exacta (sympy): el pivoteo y el redondeo no deben confundir
un error de método con un error de cuenta.
"""
from __future__ import annotations

import sympy as sp


def _matriz(x):
    return sp.Matrix(x)


def _columna(x):
    m = _matriz(x)
    if m.rows == 1 and m.cols > 1:
        return m.T
    return m


def gauss_eliminar(A, b):
    """Triangulariza ``[A|b]`` hacia adelante, sin pivoteo.

    Devuelve la matriz aumentada triangular como lista de listas.
    """
    Ab = _columna(A).row_join(_columna(b)) if _matriz(A).cols == 1 \
        else _matriz(A).row_join(_columna(b))
    n = Ab.rows
    M = [[sp.nsimplify(Ab[i, j]) for j in range(n + 1)] for i in range(n)]
    for k in range(n - 1):
        if M[k][k] == 0:
            raise ZeroDivisionError(f'pivote cero en la columna {k + 1}')
        for i in range(k + 1, n):
            m = M[i][k] / M[k][k]
            M[i] = [sp.nsimplify(M[i][j] - m * M[k][j]) for j in range(n + 1)]
    return M


def sustitucion_atras(Ab):
    """Despeja ``x`` de una matriz aumentada triangular superior.

    Devuelve una lista plana de flotantes: es lo que el alumno reporta.
    """
    if not isinstance(Ab, sp.MatrixBase):
        Ab = sp.Matrix(Ab)
    n = Ab.rows
    M = [[sp.nsimplify(Ab[i, j]) for j in range(n + 1)] for i in range(n)]
    x = [sp.Integer(0)] * n
    for i in range(n - 1, -1, -1):
        if M[i][i] == 0:
            raise ZeroDivisionError(f'pivote cero en la fila {i + 1}')
        suma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = sp.nsimplify((M[i][n] - suma) / M[i][i])
    return [float(v) for v in x]


def gauss_solve(A, b):
    """Método completo: eliminación + sustitución. Devuelve la lista de x."""
    return sustitucion_atras(sp.Matrix(gauss_eliminar(A, b)))


def lu_doolittle(A):
    """``A = L U`` con ``L`` de unos en la diagonal."""
    M = _matriz(A)
    n = M.rows
    U = [[sp.nsimplify(M[i, j]) for j in range(n)] for i in range(n)]
    L = [[sp.Integer(1) if i == j else sp.Integer(0) for j in range(n)]
         for i in range(n)]
    for k in range(n):
        if U[k][k] == 0:
            raise ZeroDivisionError(f'pivote cero en la columna {k + 1}')
        for i in range(k + 1, n):
            m = sp.nsimplify(U[i][k] / U[k][k])
            L[i][k] = m
            U[i] = [sp.nsimplify(U[i][j] - m * U[k][j]) for j in range(n)]
    return L, U


def sustitucion_adelante(L, b):
    """Resuelve ``L y = b``."""
    M = _matriz(L).row_join(_columna(b))
    n = M.rows
    A = [[sp.nsimplify(M[i, j]) for j in range(n + 1)] for i in range(n)]
    y = [sp.Integer(0)] * n
    for i in range(n):
        if A[i][i] == 0:
            raise ZeroDivisionError(f'pivote cero en la fila {i + 1}')
        suma = sum(A[i][j] * y[j] for j in range(i))
        y[i] = sp.nsimplify((A[i][n] - suma) / A[i][i])
    return y


def lu_solve(L, U, b):
    """Las dos sustituciones de la factorización. Devuelve la lista de x."""
    y = sustitucion_adelante(L, b)
    Ab = _matriz(U).row_join(sp.Matrix(y))
    return sustitucion_atras(Ab)


def residual(A, x, b):
    """``A x - b`` (para verificar, no para calificar)."""
    return _matriz(A) * sp.Matrix(x) - _columna(b)


__all__ = [
    'gauss_eliminar', 'gauss_solve', 'lu_doolittle', 'lu_solve', 'residual',
    'sustitucion_adelante', 'sustitucion_atras',
]
