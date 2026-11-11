"""visualizar — laboratorios gráficos de la Unidad 4.

`laboratorio(metodo, ej)` dibuja la figura del método y, cuando tiene sentido,
superpone TU resultado con el de la librería. No califica nada: es para ver.

Vive fuera del motor a propósito: se puede leer, copiar y modificar.
"""

import numpy as np

import matplotlib.pyplot as plt

import ajuste_curvas as ac

plt.rcParams['figure.figsize'] = (9, 4.5)


# ---------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------
def _malla(lo, hi, n=300):
    return np.linspace(lo, hi, n)


def _rango(xs, margen=0.5):
    xs = np.asarray(xs, dtype=float)
    ancho = max(xs.max() - xs.min(), 1.0)
    return xs.min() - margen * ancho, xs.max() + margen * ancho


def _estilo(ax, titulo, xlabel='x', ylabel='f(x)'):
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)


# ---------------------------------------------------------------------
# Interpolación
# ---------------------------------------------------------------------
def _lab_lineal(ej):
    d = ej['datos']
    fig, ax = plt.subplots()
    lo, hi = _rango([d['x0'], d['x1'], d['x']], 0.6)
    xs = _malla(lo, hi)
    y = ac.newton([d['x0'], d['x1']], [d['f0'], d['f1']], xs)
    ax.plot(xs, y, label='recta interpolante')
    ax.plot([d['x0'], d['x1']], [d['f0'], d['f1']], 'o', ms=8, label='nodos')
    ax.plot(d['x'], ej['f'], 's', ms=9, label=f"f({d['x']:g}) = {ej['f']:.4f}")
    ax.axvline(d['x'], color='0.7', ls=':')
    _estilo(ax, 'Interpolación lineal')
    plt.show()


def _lab_cuadratica(ej):
    d = ej['datos']
    xs_nodos = [d['x0'], d['x1'], d['x2']]
    fig, ax = plt.subplots()
    con_punto = 'x' in d
    lo, hi = _rango(xs_nodos + ([d['x']] if con_punto else []), 0.4)
    xs = _malla(lo, hi)
    ax.plot(xs, ac.newton(xs_nodos, [d['f0'], d['f1'], d['f2']], xs),
            label='parábola interpolante', lw=1.6)
    ax.plot(xs_nodos, [d['f0'], d['f1'], d['f2']], 'o', ms=8, label='nodos')
    if con_punto:
        ax.plot(d['x'], ej['f'], 's', ms=9,
                label=f"f({d['x']:g}) = {ej['f']:.4f}")
        ax.axvline(d['x'], color='0.7', ls=':')
        _estilo(ax, 'Interpolación cuadrática')
    else:
        ax.annotate(f"$b_1$ = {ej['b1']:.4f}\n$b_2$ = {ej['b2']:.4f}",
                    xy=(0.03, 0.95), xycoords='axes fraction', va='top',
                    fontsize=10,
                    bbox=dict(boxstyle='round', fc='white', ec='0.7'))
        _estilo(ax, 'Coeficientes de la parábola')
    plt.show()


def _lab_error_interp(ej):
    d = ej['datos']
    fig, ax = plt.subplots()
    xs = _malla(min(d['nodos']) - 0.5, max(d['x_todos']) + 0.5, 300)
    prod = np.ones_like(xs)
    for xi in d['nodos']:
        prod = prod * (xs - xi)
    ax.plot(xs, d['dif'] * prod,
            label=r"$R(x)=f[x_3,x_2,x_1,x_0]\prod(x-x_i)$")
    ax.plot([d['x']], [ej['R']], 's', ms=9, label=f"R = {ej['R']:.4f}")
    ax.plot(d['nodos'], [0, 0, 0], 'o', ms=8, label='nodos de la parábola')
    ax.axhline(0, color='k', lw=0.8)
    ax.axvline(d['x'], color='0.7', ls=':')
    _estilo(ax, 'Error de la interpolación (18.18)', ylabel='R(x)')
    plt.show()


# ---------------------------------------------------------------------
# Newton y Lagrange
# ---------------------------------------------------------------------
def _lab_newton_tabla(ej):
    d = ej['datos']
    fig, ax = plt.subplots()
    lo, hi = _rango(d['x'], 0.4)
    xs = _malla(lo, hi)
    ax.plot(d['x'], d['y'], 'o', ms=8, label='nodos')
    for grado, estilo in zip(range(1, len(d['x']) + 1), (':', '--', '-.', '-')):
        ax.plot(xs, ac.newton(d['x'][:grado], d['y'][:grado], xs), estilo,
                lw=1.4, label=f'grado {grado - 1}')
    _estilo(ax, 'Newton: un término más por cada nodo')
    plt.show()


def _lab_newton_eval(ej):
    d = ej['datos']
    fig, ax = plt.subplots()
    lo, hi = _rango(d['x'] + [d['xx']], 0.4)
    xs = _malla(lo, hi)
    ax.plot(xs, ac.newton(d['x'], d['y'], xs), label='polinomio de Newton')
    ax.plot(d['x'], d['y'], 'o', ms=8, label='nodos')
    ax.plot(d['xx'], ej['f'], 's', ms=9, label=f"f({d['xx']:g}) = {ej['f']:.4f}")
    ax.axvline(d['xx'], color='0.7', ls=':')
    _estilo(ax, 'Evaluación del polinomio de Newton')
    plt.show()


def _lab_lagrange(ej):
    d = ej['datos']
    fig, ax = plt.subplots()
    lo, hi = _rango(d['x'] + [d['xx']], 0.3)
    xs = _malla(lo, hi)
    for i, xi in enumerate(d['x']):
        peso = np.ones_like(xs)
        for j, xj in enumerate(d['x']):
            if i != j:
                peso = peso * (xs - xj) / (xi - xj)
        ax.plot(xs, peso, lw=1.3, label=f'$L_{i}(x)$')
    ax.plot(d['x'], np.zeros(len(d['x'])), 'o', ms=8, label='nodos')
    ax.axhline(0, color='k', lw=0.8)
    _estilo(ax, 'Pesos de Lagrange: 1 en su nodo, 0 en los demás', ylabel='$L_i(x)$')
    plt.show()


def _lab_error_newton(ej):
    d = ej['datos']
    fig, ax = plt.subplots()
    lo, hi = _rango(d['x'] + [d['xx']], 0.4)
    xs = _malla(lo, hi)
    ax.plot(xs, ac.evaluar_newton(d['x'], d['coef'], xs), label='polinomio')
    ax.plot(d['x'], [0] * len(d['x']), 'o', ms=8, label='nodos')
    ax.plot([d['xx']], [ej['R']], 's', ms=9, label=f"R = {ej['R']:.4f}")
    ax.axvline(d['xx'], color='0.7', ls=':')
    _estilo(ax, 'Término de error (18.19)')
    plt.show()


# ---------------------------------------------------------------------
# Mínimos cuadrados
# ---------------------------------------------------------------------
def _lab_regresion(ej, grado=1):
    d = ej['datos']
    r = ac.minimos_cuadrados(d['x'], d['y'], grado)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    lo, hi = _rango(d['x'], 0.3)
    xs = _malla(lo, hi)
    ax1.plot(d['x'], d['y'], 'o', ms=8, label='datos')
    ax1.plot(xs, ac.evaluar_polinomio(r['coef'], xs),
             label=f'grado {grado} · $s_{{y/x}}$ = {r["syx"]:.4f}')
    _estilo(ax1, 'Ajuste por mínimos cuadrados')
    ax2.stem(d['x'], r['residuales'], basefmt=' ')
    ax2.axhline(0, color='k', lw=0.8)
    _estilo(ax2, 'Residuales', ylabel='$e_i$')
    plt.tight_layout()
    plt.show()


def _lab_reg_lineal(ej):
    _lab_regresion(ej, 1)


def _lab_reg_cuadratica(ej):
    _lab_regresion(ej, 2)


def _lab_suma_residuos(ej):
    d = ej['datos']
    fig, ax = plt.subplots()
    modelo = [d['coef'][0] + d['coef'][1] * x for x in d['x']]
    ax.plot(d['x'], d['y'], 'o', ms=8, label='datos')
    ax.plot(d['x'], modelo, 's--', ms=6, label='modelo')
    for xi, yi, mi in zip(d['x'], d['y'], modelo):
        ax.plot([xi, xi], [mi, yi], color='tab:red', lw=1.5)
    _estilo(ax, f"Residuos al cuadrado: $S_r$ = {ej['Sr']:.4f}")
    plt.show()


def _lab_estadistico(ej, titulo, valor, etiqueta):
    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.bar([etiqueta], [valor], color='tab:blue')
    ax.bar_label(ax.containers[0], fmt='%.4f')
    ax.set_title(titulo)
    ax.grid(alpha=0.3, axis='y')
    plt.show()


# ---------------------------------------------------------------------
# Fourier
# ---------------------------------------------------------------------
def _lab_caso_gauss(ej):
    """Matriz del sistema y su solución, lado a lado."""
    d = ej['datos']
    A = np.asarray(d['A'], dtype=float)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    ax1.imshow(A, cmap='Blues')
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            ax1.text(j, i, f'{A[i, j]:g}', ha='center', va='center',
                     color='black' if abs(A[i, j]) < A.max() * 0.6 else 'white')
    ax1.set_title('Matriz del sistema')
    ax1.set_xticks([]); ax1.set_yticks([])

    x = ej['x']
    barras = ax2.bar([f'$x_{i + 1}$' for i in range(len(x))], x, color='tab:green')
    ax2.bar_label(barras, fmt='%.4g')
    ax2.axhline(0, color='k', lw=0.8)
    ax2.set_title('Solución del sistema')
    ax2.grid(alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()


def _lab_fourier(ej):
    d = ej['datos']
    coef = {'A0': d['y'] and np.mean(d['y']), 'A': [], 'B': []}
    coef['A0'], coef['A'], coef['B'] = [ej['A0']], [ej['A1']], [ej['B1']]
    t = np.asarray(d['t'])
    y = np.asarray(d['y'])
    tt = _malla(t.min(), t.max(), 300)
    modelo = ej['A0'] + ej['A1'] * np.cos(d['omega0'] * tt) \
        + ej['B1'] * np.sin(d['omega0'] * tt)
    fig, ax = plt.subplots()
    ax.plot(t, y, 'o', ms=8, label='muestras')
    ax.plot(tt, modelo, label='serie con m = 1')
    ax.axhline(ej['A0'], color='0.6', ls=':', label='$A_0$')
    _estilo(ax, 'Ajuste con serie de Fourier', xlabel='t', ylabel='y')
    plt.show()


# ---------------------------------------------------------------------
# Despacho
# ---------------------------------------------------------------------
_LABS = {
    'INTERP_LINEAL': _lab_lineal,
    'COEF_CUADRATICOS': _lab_cuadratica,
    'INTERP_CUADRATICA': _lab_cuadratica,
    'ERROR_INTERP': _lab_error_interp,
    'NEWTON_TABLA': _lab_newton_tabla,
    'NEWTON_EVAL': _lab_newton_eval,
    'LAGRANGE': _lab_lagrange,
    'ERROR_NEWTON': _lab_error_newton,
    'SUMA_RESIDUOS': _lab_suma_residuos,
    'REG_LINEAL': _lab_reg_lineal,
    'REG_CUADRATICA': _lab_reg_cuadratica,
    'ERROR_ESTANDAR': lambda ej: _lab_estadistico(
        ej, 'Error estándar de la estimación', ej['syx'], '$s_{y/x}$'),
    'COEF_DETERMINACION': lambda ej: _lab_estadistico(
        ej, 'Coeficiente de determinación', ej['r2'], '$r^2$'),
    'CASO_GAUSS': _lab_caso_gauss,
    'CASO_NORMALES': _lab_reg_lineal,
    'FOURIER': _lab_fourier,
}


def laboratorio(metodo, ej):
    """Dibuja el laboratorio del método con el ejercicio del alumno."""
    fn = _LABS.get(metodo)
    if fn is None:
        print(f'Sin laboratorio para {metodo!r}.')
        return
    fn(ej)


__all__ = ['laboratorio']
