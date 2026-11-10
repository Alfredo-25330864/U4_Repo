"""Fábrica de preguntas de la Unidad 4.

Cada método completo tiene UNA pregunta de programar con casos ocultos: el
alumno escribe la función y aquí se prueba con datos que NO son los de su
actividad a mano (semilla distinta), así copiar el enunciado no sirve.

Los valores esperados los calcula ``solvers_u4``, nunca una fórmula escrita a
mano: si el solver cambia, la pregunta cambia con él.
"""
from __future__ import annotations

import mn_motor.comun as comun
import mn_motor.ejercicios_u4 as catalogo
import mn_motor.solvers_u4 as sol


def _datos_lineal(rng):
    x0 = int(rng.integers(0, 6))
    x1 = x0 + int(rng.integers(2, 5))
    f0 = int(rng.integers(-4, 7))
    f1 = f0 + int(rng.integers(-6, 7))
    x = x0 + 1
    return (float(x0), float(f0), float(x1), float(f1), float(x))


def _datos_cuadratica(rng):
    x0 = int(rng.integers(0, 3))
    x1 = x0 + int(rng.integers(1, 3))
    x2 = x1 + int(rng.integers(1, 3))
    a, b, c = int(rng.integers(1, 4)), int(rng.integers(-4, 4)), int(rng.integers(-5, 6))
    f = lambda t: a * t ** 2 + b * t + c          # noqa: E731
    return (float(x0), float(f(x0)), float(x1), float(f(x1)),
            float(x2), float(f(x2)), float(x0 + 1.5))


def _nodos(rng, n):
    xs = list(rng.choice(range(0, 7), size=n, replace=False))
    xs = [int(v) for v in sorted(xs)]
    coefs = [int(rng.integers(1, 4)) for _ in range(n)]
    ys = [sum(c * x ** k for k, c in enumerate(coefs)) for x in xs]
    return [float(v) for v in xs], [float(v) for v in ys]


def _datos_newton_tabla(rng):
    return tuple(_nodos(rng, 4))


def _datos_newton_eval(rng):
    xs, ys = _nodos(rng, 4)
    return (xs, ys, float(xs[1] + 0.5))


def _datos_lagrange(rng):
    xs, ys = _nodos(rng, 4)
    return (xs, ys, float(xs[1] + 0.5))


def _datos_reg_lineal(rng):
    xs = [float(v) for v in range(1, 6)]
    a1 = int(rng.integers(-3, 4))
    a0 = int(rng.integers(-3, 5))
    ys = [a0 + a1 * x + int(rng.integers(-1, 2)) for x in xs]
    return (xs, [float(v) for v in ys])


def _datos_reg_cuadratica(rng):
    xs = [float(v) for v in range(0, 6)]
    a2, a1, a0 = (int(rng.integers(1, 4)), int(rng.integers(-3, 4)),
                  int(rng.integers(-3, 5)))
    ys = [a0 + a1 * x + a2 * x ** 2 + int(rng.integers(-1, 2)) for x in xs]
    return (xs, [float(v) for v in ys])


def _datos_fourier(rng):
    import math

    N = 8
    omega0 = 2 * math.pi               # un periodo completo en t = [0, 1)
    ts = [k / N for k in range(N)]
    A0, A1, B1 = (float(rng.integers(0, 4)), float(rng.integers(1, 4)),
                  float(rng.integers(1, 4)))
    ys = [A0 + A1 * math.cos(omega0 * t) + B1 * math.sin(omega0 * t) for t in ts]
    return (ts, ys, omega0, 1)


def _datos_coef_cuadraticos(rng):
    x0 = int(rng.integers(0, 3))
    x1 = x0 + int(rng.integers(1, 3))
    x2 = x1 + int(rng.integers(1, 3))
    a, b, c = int(rng.integers(1, 4)), int(rng.integers(-4, 4)), int(rng.integers(-5, 6))
    f = lambda t: a * t ** 2 + b * t + c          # noqa: E731
    return (float(x0), float(f(x0)), float(x1), float(f(x1)),
            float(x2), float(f(x2)))


def _datos_error_interp(rng):
    xs, ys = _nodos(rng, 4)
    from mn_motor.solvers_u4 import tabla_diferencias
    dif = float(tabla_diferencias(xs, ys)[3][3])
    return (dif, xs[:3], float(xs[1] + 0.5))


def _datos_error_newton(rng):
    xs, ys = _nodos(rng, 4)
    from mn_motor.solvers_u4 import coeficientes_newton
    coef = [float(v) for v in coeficientes_newton(xs, ys)]
    return (xs, coef, float(xs[1] + 0.5))


def _datos_suma_residuos(rng):
    xs = [float(v) for v in range(1, 6)]
    a1 = int(rng.integers(1, 4))
    a0 = int(rng.integers(0, 5))
    ys = [float(a0 + a1 * x + int(rng.integers(-2, 3))) for x in xs]
    coef = [float(a0) + 0.5, float(a1) - 0.25]
    return (xs, ys, coef)


def _datos_error_estandar(rng):
    n = int(rng.integers(6, 10))
    m = int(rng.integers(0, 3))
    if n - (m + 1) <= 0:
        m = 0
    sr = float(int(rng.integers(2, 40)) + int(rng.integers(0, 10)) / 4)
    return (sr, n, m)


def _datos_coef_determinacion(rng):
    st = float(int(rng.integers(40, 200)))
    sr = float(int(rng.integers(1, 30)) + int(rng.integers(0, 4)) / 4)
    return (sr, st)


def _datos_caso_gauss(rng):
    while True:
        A = [[float(rng.integers(-3, 4)) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            otros = sum(abs(A[i][j]) for j in range(3) if j != i)
            A[i][i] = otros + float(rng.integers(1, 4))
        sol = [float(rng.integers(-3, 4)) for _ in range(3)]
        b = [sum(A[i][j] * sol[j] for j in range(3)) for i in range(3)]
        if any(v == 0 for v in sol):
            continue
        return (A, b)


def _datos_caso_normales(rng):
    xs = [float(v) for v in (0, 10, 20, 30, 40)]
    a1 = int(rng.integers(1, 4))
    a0 = int(rng.integers(0, 5))
    ys = [float(a0 + a1 * x + int(rng.integers(-1, 2))) for x in xs]
    return (xs, ys, 1)


_DATOS = {
    'INTERP_LINEAL': _datos_lineal,
    'COEF_CUADRATICOS': _datos_coef_cuadraticos,
    'INTERP_CUADRATICA': _datos_cuadratica,
    'ERROR_INTERP': _datos_error_interp,
    'NEWTON_TABLA': _datos_newton_tabla,
    'NEWTON_EVAL': _datos_newton_eval,
    'LAGRANGE': _datos_lagrange,
    'ERROR_NEWTON': _datos_error_newton,
    'SUMA_RESIDUOS': _datos_suma_residuos,
    'REG_LINEAL': _datos_reg_lineal,
    'REG_CUADRATICA': _datos_reg_cuadratica,
    'ERROR_ESTANDAR': _datos_error_estandar,
    'COEF_DETERMINACION': _datos_coef_determinacion,
    'CASO_GAUSS': _datos_caso_gauss,
    'CASO_NORMALES': _datos_caso_normales,
    'FOURIER': _datos_fourier,
}


def _modulo_de(metodo):
    """El módulo de referencia del método: U4 para casi todo, U3 para Gauss."""
    import mn_motor.solvers_u3 as u3

    nombre = catalogo.NOMBRE_FUNCION[metodo]
    if hasattr(sol, nombre):
        return sol
    if hasattr(u3, nombre):
        return u3
    raise AttributeError(f'no hay referencia para {metodo!r} ({nombre})')


def _esperado(metodo, entrada):
    """Valor de referencia para una entrada, con el solver del motor."""
    modulo = _modulo_de(metodo)
    fn = getattr(modulo, catalogo.NOMBRE_FUNCION[metodo])
    return _a_tipos_simples(fn(*entrada))


def _a_tipos_simples(valor):
    """sympy/Matrix -> float o lista de floats, para comparar sin sustos."""
    if isinstance(valor, (list, tuple)):
        return [_a_tipos_simples(v) for v in valor]
    try:
        return float(valor)
    except (TypeError, ValueError):
        return valor


class PreguntaFuncion:
    """Pregunta de programar: el alumno escribe el método y se prueban casos."""

    def __init__(self, metodo, n_casos=3, peso=100):
        self.metodo = metodo
        self.n_casos = n_casos
        self.peso = peso

    def construir(self, semilla):
        rng = comun.rng_de(semilla, 7_000 + catalogo.METODOS.index(self.metodo))
        casos = []
        for _ in range(self.n_casos):
            entrada = _DATOS[self.metodo](rng)
            casos.append((entrada, _esperado(self.metodo, entrada)))

        # El ejemplo visible usa un sorteo aparte y SÍ puede ser el del
        # enunciado: sirve para que el alumno compruebe antes de enviar.
        rng_ej = comun.rng_de(semilla, 9_000 + catalogo.METODOS.index(self.metodo))
        entrada_ej = _DATOS[self.metodo](rng_ej)
        ejemplo = (entrada_ej, _esperado(self.metodo, entrada_ej))

        return {
            'tipo': 'funcion',
            'id': f"f_{self.metodo.lower()}",
            'titulo': catalogo.NOMBRE_METODO[self.metodo],
            'enunciado': (
                f"Programa `{catalogo.NOMBRE_FUNCION[self.metodo]}` con el "
                f"algoritmo de **{catalogo.NOMBRE_METODO[self.metodo]}**. "
                'El método debe llamar a sus pasos sueltos.'),
            'funcion': catalogo.NOMBRE_FUNCION[self.metodo],
            'firma': f"{catalogo.NOMBRE_FUNCION[self.metodo]}(...)",
            'casos': casos,
            'ejemplo': ejemplo,
            'referencia': catalogo.NOMBRE_FUNCION[self.metodo],
            'peso': self.peso,
        }


def preguntas_de(metodos, peso=100):
    """Preguntas de programar para una lista de métodos."""
    return [PreguntaFuncion(m, peso=peso) for m in metodos]


__all__ = ['PreguntaFuncion', 'preguntas_de']
