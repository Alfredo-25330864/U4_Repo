"""Catálogo de ejercicios sembrados de la Unidad 4.

Cada método —incluidas las piezas que calculan un error o una suma— tiene una
fábrica que sortea datos con el RNG del alumno y deja calculada la referencia
con ``solvers_u4``. Los números son pequeños y enteros: la actividad es a mano
y con calculadora.

``METODOS`` fija el orden de los bloques del cuaderno. Qué reporta el alumno
en cada actividad se declara en ``MANO_REPORTE`` como pares
``(etiqueta, función_del_ejercicio)``.
"""
from __future__ import annotations

import sympy as sp

import mn_motor.solvers_u4 as sol

# ---------------------------------------------------------------------
# Orden de los métodos: es el orden de los bloques del cuaderno.
# Se agrupan por cuaderno: 01 interpolación, 02 Newton/Lagrange,
# 03 mínimos cuadrados, 04 casos + Fourier (tarea extra).
# ---------------------------------------------------------------------
METODOS = (
    'INTERP_LINEAL',
    'COEF_CUADRATICOS',
    'INTERP_CUADRATICA',
    'ERROR_INTERP',
    'NEWTON_TABLA',
    'NEWTON_EVAL',
    'LAGRANGE',
    'ERROR_NEWTON',
    'SUMA_RESIDUOS',
    'REG_LINEAL',
    'REG_CUADRATICA',
    'ERROR_ESTANDAR',
    'COEF_DETERMINACION',
    'FOURIER',
)

NOMBRE_METODO = {
    'INTERP_LINEAL': 'Interpolación lineal',
    'COEF_CUADRATICOS': 'Coeficientes de la parábola',
    'INTERP_CUADRATICA': 'Interpolación cuadrática',
    'ERROR_INTERP': 'Error de interpolación con punto extra',
    'NEWTON_TABLA': 'Tabla de diferencias divididas',
    'NEWTON_EVAL': 'Polinomio de Newton',
    'LAGRANGE': 'Polinomio de Lagrange',
    'ERROR_NEWTON': 'Error del polinomio de Newton',
    'SUMA_RESIDUOS': 'Suma de residuos al cuadrado',
    'REG_LINEAL': 'Regresión lineal',
    'REG_CUADRATICA': 'Regresión cuadrática',
    'ERROR_ESTANDAR': 'Error estándar de la estimación',
    'COEF_DETERMINACION': 'Coeficiente de determinación',
    'FOURIER': 'Serie de Fourier (tarea extra)',
}

# Nombre EXACTO de la función que programa el alumno.
NOMBRE_FUNCION = {
    'INTERP_LINEAL': 'interpolacion_lineal',
    'COEF_CUADRATICOS': 'coeficientes_cuadraticos',
    'INTERP_CUADRATICA': 'interpolacion_cuadratica',
    'ERROR_INTERP': 'error_estimado_interpolacion',
    'NEWTON_TABLA': 'coeficientes_newton',
    'NEWTON_EVAL': 'interpolacion_newton',
    'LAGRANGE': 'interpolacion_lagrange',
    'ERROR_NEWTON': 'error_newton',
    'SUMA_RESIDUOS': 'suma_residuos_cuadrados',
    'REG_LINEAL': 'regresion_lineal',
    'REG_CUADRATICA': 'regresion_cuadratica',
    'ERROR_ESTANDAR': 'error_estandar',
    'COEF_DETERMINACION': 'coeficiente_determinacion',
    'FOURIER': 'coeficientes_fourier',
}

# Pieza suelta asociada al método (la que el método completo debe llamar).
NOMBRE_PIEZA = {
    'INTERP_LINEAL': 'interpolacion_lineal',
    'COEF_CUADRATICOS': 'coeficientes_cuadraticos',
    'INTERP_CUADRATICA': 'coeficientes_cuadraticos',
    'ERROR_INTERP': 'error_estimado_interpolacion',
    'NEWTON_TABLA': 'tabla_diferencias',
    'NEWTON_EVAL': 'evaluar_newton',
    'LAGRANGE': 'interpolacion_lagrange',
    'ERROR_NEWTON': 'error_newton',
    'SUMA_RESIDUOS': 'suma_residuos_cuadrados',
    'REG_LINEAL': 'regresion_lineal',
    'REG_CUADRATICA': 'regresion_cuadratica',
    'ERROR_ESTANDAR': 'error_estandar',
    'COEF_DETERMINACION': 'coeficiente_determinacion',
    'FOURIER': 'coeficientes_fourier',
}

# Qué métodos van a cada cuaderno (el orden importa).
CUADERNO_METODOS = {
    'u4_01_interpolacion': ('INTERP_LINEAL', 'COEF_CUADRATICOS',
                            'INTERP_CUADRATICA', 'ERROR_INTERP'),
    'u4_02_newton_lagrange': ('NEWTON_TABLA', 'NEWTON_EVAL', 'LAGRANGE',
                              'ERROR_NEWTON'),
    'u4_03_minimos_cuadrados': ('SUMA_RESIDUOS', 'REG_LINEAL',
                                'REG_CUADRATICA', 'ERROR_ESTANDAR',
                                'COEF_DETERMINACION'),
    'u4_04_casos': ('FOURIER',),
}


def _num(v, dec=4):
    """Número -> texto corto para el enunciado."""
    v = float(v)
    if abs(v - round(v)) < 1e-12 and abs(v) < 1e6:
        return str(int(round(v)))
    return f'{v:.{dec}f}'.rstrip('0').rstrip('.')


def _lista(vals):
    return ', '.join(_num(v) for v in vals)


def _tabla(xs, ys):
    xs = ' | '.join(str(int(v)) if float(v).is_integer() else _num(v) for v in xs)
    ys = ' | '.join(_num(v) for v in ys)
    return (f'| $x$ | {xs} |\n|{"---|" * (len(list(xs.split(" | "))) + 1)}\n'
            f'| $f(x)$ | {ys} |')


def _polinomio_y_nodos(rng, cuantos=4):
    """Nodos distintos con valores de un polinomio de coeficientes pequeños."""
    xs = sorted(int(v) for v in rng.choice(range(0, 7), size=cuantos, replace=False))
    coefs = [int(rng.integers(1, 4)) for _ in range(cuantos)]
    ys = [sum(c * x ** k for k, c in enumerate(coefs)) for x in xs]
    return xs, ys


# =====================================================================
# 4.1 — Interpolación
# =====================================================================
def _ej_interp_lineal(rng):
    x0 = int(rng.integers(1, 5))
    x1 = x0 + int(rng.integers(2, 4))
    f0 = int(rng.integers(1, 8))
    f1 = f0 + int(rng.integers(2, 9))
    x = x0 + 1
    ref = float(sol.interpolacion_lineal(x0, f0, x1, f1, x))
    return {
        'tipo': 'INTERP_LINEAL',
        'titulo': f'Recta por ({x0}, {f0}) y ({x1}, {f1})',
        'contexto': (f'Se conocen dos valores: $f({x0}) = {f0}$ y '
                     f'$f({x1}) = {f1}$.\n\n'
                     f'Estima $f({x})$ por interpolación lineal, ecuación (18.2).'),
        'datos': {'x0': float(x0), 'f0': float(f0), 'x1': float(x1),
                  'f1': float(f1), 'x': float(x)},
        'f': ref,
    }


def _ej_coef_cuadraticos(rng):
    x0 = 1
    x1 = int(rng.integers(2, 4))
    x2 = x1 + int(rng.integers(1, 3))
    a, b, c = int(rng.integers(1, 3)), int(rng.integers(-3, 3)), int(rng.integers(1, 7))
    f = lambda t: a * t ** 2 + b * t + c          # noqa: E731
    f0, f1, f2 = f(x0), f(x1), f(x2)
    b0, b1, b2 = sol.coeficientes_cuadraticos(x0, f0, x1, f1, x2, f2)
    return {
        'tipo': 'COEF_CUADRATICOS',
        'titulo': f'Parábola por ({x0}, {f0}), ({x1}, {f1}) y ({x2}, {f2})',
        'contexto': ('Ajusta la parábola que pasa por\n\n'
                     + _tabla([x0, x1, x2], [f0, f1, f2])
                     + '\n\nCalcula $b_1$ con (18.5) y $b_2$ con (18.6).'),
        'datos': {'x0': float(x0), 'f0': float(f0), 'x1': float(x1),
                  'f1': float(f1), 'x2': float(x2), 'f2': float(f2)},
        'b1': float(b1), 'b2': float(b2),
    }


def _ej_interp_cuadratica(rng):
    base = _ej_coef_cuadraticos(rng)
    d = base['datos']
    x = d['x0'] + 1.5
    ref = float(sol.interpolacion_cuadratica(d['x0'], d['f0'], d['x1'], d['f1'],
                                             d['x2'], d['f2'], x))
    base.update({
        'tipo': 'INTERP_CUADRATICA',
        'titulo': base['titulo'] + f' · evalúa en {_num(x)}',
        'contexto': base['contexto'] + f'\n\nEstima $f({_num(x)})$ con (18.3).',
        'datos': {**d, 'x': float(x)},
        'f': ref,
    })
    return base


def _ej_error_interp(rng):
    xs = sorted(int(v) for v in rng.choice(range(1, 7), size=4, replace=False))
    coefs = [int(rng.integers(1, 4)) for _ in range(4)]
    ys = [sum(c * x ** k for k, c in enumerate(coefs)) for x in xs]
    tabla = sol.tabla_diferencias(xs, ys)
    dif = float(tabla[3][3])
    x = float(xs[1] + 0.5)
    ref = float(sol.error_estimado_interpolacion(dif, xs[:3], x))
    return {
        'tipo': 'ERROR_INTERP',
        'titulo': f'Error con punto extra en $x = {_num(x)}$',
        'contexto': ('Con los nodos $x = %s$, la tercera diferencia dividida es '
                     '$f[x_3,x_2,x_1,x_0] = %s$.\n\n'
                     'Estima el error de la parábola en $x = %s$ con (18.18).'
                     % (_lista(xs), _num(dif), _num(x))),
        'datos': {'nodos': [float(v) for v in xs[:3]], 'x': x,
                  'dif': dif, 'x_todos': [float(v) for v in xs]},
        'R': ref,
    }


# =====================================================================
# 4.2 — Newton y Lagrange
# =====================================================================
def _ej_newton_tabla(rng):
    xs, ys = _polinomio_y_nodos(rng, 4)
    b = [float(v) for v in sol.coeficientes_newton(xs, ys)]
    return {
        'tipo': 'NEWTON_TABLA',
        'titulo': 'Diferencias divididas de cuatro nodos',
        'contexto': ('Construye la tabla de diferencias divididas para\n\n'
                     + _tabla(xs, ys)
                     + '\n\nReporta $b_0, b_1, b_2, b_3$ (la diagonal).'),
        'datos': {'x': [float(v) for v in xs], 'y': [float(v) for v in ys]},
        'b': b,
    }


def _ej_newton_eval(rng):
    xs, ys = _polinomio_y_nodos(rng, 4)
    b = sol.coeficientes_newton(xs, ys)
    xx = float(xs[1] + 0.5)
    return {
        'tipo': 'NEWTON_EVAL',
        'titulo': f'Polinomio de Newton en $x = {_num(xx)}$',
        'contexto': ('Con los nodos\n\n' + _tabla(xs, ys)
                     + f'\n\nevalúa el polinomio de Newton (18.7) en '
                       f'$x = {_num(xx)}$.'),
        'datos': {'x': [float(v) for v in xs], 'y': [float(v) for v in ys],
                  'xx': xx},
        'f': float(sol.evaluar_newton(xs, b, xx)),
    }


def _ej_lagrange(rng):
    xs = [1, 2, 4, 5]
    coefs = [int(rng.integers(1, 4)) for _ in range(4)]
    ys = [sum(c * x ** k for k, c in enumerate(coefs)) for x in xs]
    xx = 3.0
    return {
        'tipo': 'LAGRANGE',
        'titulo': 'Lagrange con nodos no equidistantes',
        'contexto': ('Con los nodos\n\n' + _tabla(xs, ys)
                     + f'\n\nevalúa el polinomio de Lagrange (18.20) en '
                       f'$x = {_num(xx)}$.'),
        'datos': {'x': [float(v) for v in xs], 'y': [float(v) for v in ys],
                  'xx': xx},
        'f': float(sol.interpolacion_lagrange(xs, ys, xx)),
    }


def _ej_error_newton(rng):
    xs, ys = _polinomio_y_nodos(rng, 4)
    b = [float(v) for v in sol.coeficientes_newton(xs, ys)]
    xx = float(xs[1] + 0.5)
    return {
        'tipo': 'ERROR_NEWTON',
        'titulo': f'Error del cúbico en $x = {_num(xx)}$',
        'contexto': (f'La tabla de diferencias divididas dio '
                     f'$b = [%s]$ con nodos $x = %s$.\n\n'
                     'Reporta la estimación del error del polinomio de grado 3 '
                     'en $x = %s$, ecuación (18.19).'
                     % (_lista(b), _lista(xs), _num(xx))),
        'datos': {'x': [float(v) for v in xs], 'coef': b, 'xx': xx},
        'R': float(sol.error_newton(xs, b, xx)),
    }


# =====================================================================
# 4.3 — Mínimos cuadrados
# =====================================================================
def _ej_suma_residuos(rng):
    xs = [1, 2, 3, 4, 5]
    a1 = int(rng.integers(1, 4))
    a0 = int(rng.integers(0, 5))
    ys = [a0 + a1 * x + int(rng.integers(-2, 3)) for x in xs]
    coef = [float(a0) + 0.5, float(a1) - 0.25]
    sr = float(sol.suma_residuos_cuadrados(xs, ys, coef))
    return {
        'tipo': 'SUMA_RESIDUOS',
        'titulo': 'Suma de residuos al cuadrado',
        'contexto': ('Con los datos\n\n' + _tabla(xs, ys)
                     + '\ny el modelo $y = %s + %s x$, calcula $S_r$ con (17.3).'
                     % (_num(coef[0]), _num(coef[1]))),
        'datos': {'x': [float(v) for v in xs], 'y': [float(v) for v in ys],
                  'coef': coef},
        'Sr': sr,
    }


def _ej_reg_lineal(rng):
    xs = [1, 2, 3, 4, 5]
    a1 = int(rng.integers(1, 4))
    a0 = int(rng.integers(0, 5))
    ys = [a0 + a1 * x + int(rng.integers(-1, 2)) for x in xs]
    coef = [float(v) for v in sol.regresion_lineal(xs, ys)]
    sr = float(sol.suma_residuos_cuadrados(xs, ys, coef))
    st = float(sol.suma_cuadrados_total(ys))
    return {
        'tipo': 'REG_LINEAL',
        'titulo': 'Ajuste lineal de cinco puntos',
        'contexto': ('Ajusta una recta por mínimos cuadrados a\n\n'
                     + _tabla(xs, ys)
                     + '\n\nReporta $a_0$, $a_1$ y $S_r$ (17.3).'),
        'datos': {'x': [float(v) for v in xs], 'y': [float(v) for v in ys]},
        'a0': coef[0], 'a1': coef[1], 'Sr': sr, 'St': st,
        'r2': float(sol.coeficiente_determinacion(sr, st)),
    }


def _ej_reg_cuadratica(rng):
    xs = [0, 1, 2, 3, 4, 5]
    a2 = int(rng.integers(1, 4))
    a1 = int(rng.integers(-2, 3))
    a0 = int(rng.integers(0, 5))
    ys = [a0 + a1 * x + a2 * x ** 2 + int(rng.integers(-1, 2)) for x in xs]
    coef = [float(v) for v in sol.regresion_cuadratica(xs, ys)]
    sr = float(sol.suma_residuos_cuadrados(xs, ys, coef))
    st = float(sol.suma_cuadrados_total(ys))
    return {
        'tipo': 'REG_CUADRATICA',
        'titulo': 'Ajuste cuadrático de seis puntos',
        'contexto': ('Ajusta una parábola por mínimos cuadrados a\n\n'
                     + _tabla(xs, ys)
                     + '\n\nReporta $a_0$, $a_1$, $a_2$ y $r^2$ (17.10).'),
        'datos': {'x': [float(v) for v in xs], 'y': [float(v) for v in ys]},
        'a0': coef[0], 'a1': coef[1], 'a2': coef[2],
        'Sr': sr, 'St': st,
        'r2': float(sol.coeficiente_determinacion(sr, st)),
    }


def _ej_error_estandar(rng):
    n = int(rng.integers(6, 10))
    m = int(rng.integers(0, 3))
    if n - (m + 1) <= 0:
        m = 0
    sr = float(int(rng.integers(2, 40)) + int(rng.integers(0, 10)) / 4)
    ref = float(sol.error_estandar(sr, n, m))
    return {
        'tipo': 'ERROR_ESTANDAR',
        'titulo': 'Error estándar de la estimación',
        'contexto': (f'Un ajuste con $n = {n}$ datos y grado $m = {m}$ dejó '
                     f'$S_r = {_num(sr)}$.\n\n'
                     'Reporta el error estándar $s_{y/x}$ con (17.20).'),
        'datos': {'Sr': sr, 'n': n, 'm': m},
        'syx': ref,
    }


def _ej_coef_determinacion(rng):
    st = float(int(rng.integers(40, 200)))
    sr = float(int(rng.integers(1, 30)) + int(rng.integers(0, 4)) / 4)
    ref = float(sol.coeficiente_determinacion(sr, st))
    return {
        'tipo': 'COEF_DETERMINACION',
        'titulo': 'Coeficiente de determinación',
        'contexto': (f'Un ajuste dejó $S_r = {_num(sr)}$ y la suma total es '
                     f'$S_t = {_num(st)}$.\n\n'
                     'Reporta $r^2$ con (17.10) y $r=\\sqrt{r^2}$.'),
        'datos': {'Sr': sr, 'St': st},
        'r2': ref, 'r': float(abs(ref) ** 0.5),
    }


# =====================================================================
# Tarea extra — Fourier
# =====================================================================
def _ej_fourier(rng):
    A0 = int(rng.integers(1, 4))
    A1 = int(rng.integers(1, 4))
    B1 = int(rng.integers(1, 4))
    N = 8
    w = 2 * sp.pi                      # un periodo completo en t = [0, 1)
    ts = [k / N for k in range(N)]
    ys = [float(A0 + A1 * sp.cos(w * t) + B1 * sp.sin(w * t)) for t in ts]
    A0c, A, B = sol.coeficientes_fourier(ts, ys, float(w), 1)
    return {
        'tipo': 'FOURIER',
        'titulo': 'Coeficientes de una sinusoide',
        'contexto': (f'Se muestreó una señal en $N = {N}$ puntos de un periodo '
                     f'($t \\in [0, 1)$, $\\Delta t = 1/{N}$), con '
                     f'$\\omega_0 = 2\\pi$.\n\n'
                     + '| $t$ | ' + ' | '.join(f'{t:.3f}' for t in ts) + ' |\n'
                     + '|---|' + '---|' * N + '\n'
                     + '| $y$ | ' + ' | '.join(f'{v:.4f}' for v in ys) + ' |\n\n'
                     + 'Reporta $A_0$, $A_1$ y $B_1$ con (19.14)–(19.16).'),
        'datos': {'t': ts, 'y': ys, 'omega0': float(w), 'N': N},
        'A0': float(A0c), 'A1': float(A[0]), 'B1': float(B[0]),
    }


MANO_FABRICA = {
    'INTERP_LINEAL': [_ej_interp_lineal],
    'COEF_CUADRATICOS': [_ej_coef_cuadraticos],
    'INTERP_CUADRATICA': [_ej_interp_cuadratica],
    'ERROR_INTERP': [_ej_error_interp],
    'NEWTON_TABLA': [_ej_newton_tabla],
    'NEWTON_EVAL': [_ej_newton_eval],
    'LAGRANGE': [_ej_lagrange],
    'ERROR_NEWTON': [_ej_error_newton],
    'SUMA_RESIDUOS': [_ej_suma_residuos],
    'REG_LINEAL': [_ej_reg_lineal],
    'REG_CUADRATICA': [_ej_reg_cuadratica],
    'ERROR_ESTANDAR': [_ej_error_estandar],
    'COEF_DETERMINACION': [_ej_coef_determinacion],
    'FOURIER': [_ej_fourier],
}

MANO_REPORTE = {
    'INTERP_LINEAL': (('f(x)', lambda ej: ej['f']),),
    'COEF_CUADRATICOS': (('b_1', lambda ej: ej['b1']),
                         ('b_2', lambda ej: ej['b2'])),
    'INTERP_CUADRATICA': (('f(x)', lambda ej: ej['f']),),
    'ERROR_INTERP': (('R_2', lambda ej: ej['R']),),
    'NEWTON_TABLA': (('b_0', lambda ej: ej['b'][0]),
                     ('b_1', lambda ej: ej['b'][1]),
                     ('b_2', lambda ej: ej['b'][2]),
                     ('b_3', lambda ej: ej['b'][3])),
    'NEWTON_EVAL': (('f(x)', lambda ej: ej['f']),),
    'LAGRANGE': (('f(x)', lambda ej: ej['f']),),
    'ERROR_NEWTON': (('R_3', lambda ej: ej['R']),),
    'SUMA_RESIDUOS': (('S_r', lambda ej: ej['Sr']),),
    'REG_LINEAL': (('a_0', lambda ej: ej['a0']),
                   ('a_1', lambda ej: ej['a1']),
                   ('S_r', lambda ej: ej['Sr'])),
    'REG_CUADRATICA': (('a_0', lambda ej: ej['a0']),
                       ('a_1', lambda ej: ej['a1']),
                       ('a_2', lambda ej: ej['a2']),
                       ('r^2', lambda ej: ej['r2'])),
    'ERROR_ESTANDAR': (('s_{y/x}', lambda ej: ej['syx']),),
    'COEF_DETERMINACION': (('r^2', lambda ej: ej['r2']),),
    'FOURIER': (('A_0', lambda ej: ej['A0']),
                ('A_1', lambda ej: ej['A1']),
                ('B_1', lambda ej: ej['B1'])),
}


def elegir_mano(metodo, rng):
    """Sortea el ejercicio del método con el RNG del alumno."""
    fabricas = MANO_FABRICA[metodo]
    return fabricas[int(rng.integers(0, len(fabricas)))](rng)


def referencia(metodo, ej):
    """Valores de referencia del ejercicio, como pares (etiqueta, valor)."""
    return [(etq, float(fn(ej))) for etq, fn in MANO_REPORTE[metodo]]


__all__ = [
    'CUADERNO_METODOS', 'MANO_FABRICA', 'MANO_REPORTE', 'METODOS',
    'NOMBRE_FUNCION', 'NOMBRE_METODO', 'NOMBRE_PIEZA', 'elegir_mano',
    'referencia',
]
