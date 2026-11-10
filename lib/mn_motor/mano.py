"""Actividades a mano: enunciado sembrado, comprobación y resumen final.

Cada método tiene una actividad a mano con datos distintos por alumno. El
alumno reporta números truncados/redondeados a 4 decimales y aquí se comparan
con la referencia exacta del solver.

El flujo del cuaderno es: por cada método se llama ``mano_enunciado`` (muestra
el problema) y después ``mano_comprueba`` (revisa los valores). Al final, una
sola celda resume todas con ``mano_comprueba_todos``.
"""
from __future__ import annotations

import mn_motor.comun as comun
import mn_motor.ejercicios_u4 as catalogo
import mn_motor.tarea as tarea

# Tolerancia relativa de las actividades a mano. El alumno reporta 4 decimales:
# truncar y redondear difieren como mucho 1e-4, así que 1.5e-4 acepta ambos sin
# dejar pasar un error de tercer decimal.
TOL_MANO = 1.5e-4

_MANO = {}      # metodo -> valores reportados
_MANO_EJ = {}   # metodo -> ejercicio sorteado
_MANO_OK = {}   # metodo -> True si todos los valores son correctos


def _display(*objetos):
    from IPython.display import display
    display(*objetos)


def _markdown(texto):
    from IPython.display import Markdown
    return Markdown(texto)


def _alumno_id(nc=None):
    if nc:
        return nc
    return tarea.tarea_activa()['alumno_id']


def _sal(metodo):
    """Desplazamiento estable de la semilla por método.

    No se usa ``hash()``: Python aleatoriza el hash de los textos entre
    ejecuciones y el ejercicio del alumno cambiaría cada vez.
    """
    return 1_000 + catalogo.METODOS.index(metodo) * 101


def mano_enunciado(metodo, nc=None):
    """Muestra el enunciado de la actividad a mano y guarda el ejercicio.

    Devuelve el diccionario del ejercicio; el cuaderno usa ``EJ['datos']`` para
    llamar a la función del alumno.
    """
    if metodo not in catalogo.MANO_FABRICA:
        raise ValueError(f'método desconocido: {metodo!r}')

    alumno = _alumno_id(nc)
    rng = comun.rng_de(alumno, _sal(metodo))
    ej = catalogo.elegir_mano(metodo, rng)
    _MANO_EJ[metodo] = ej

    etiquetas = ',\\ '.join(f'${etq}$' for etq, _ in catalogo.MANO_REPORTE[metodo])
    _display(_markdown(
        f'#### ✏️ {catalogo.NOMBRE_METODO[metodo]} — actividad a mano\n\n'
        f'{ej["contexto"]}\n\n'
        f'>>> Reporta **{etiquetas}** con 4 decimales.'))
    return ej


def mano_comprueba(metodo, valores):
    """Comprueba los valores reportados. Devuelve True/False.

    No revela la referencia: sólo dice si cada valor quedó dentro de la
    tolerancia, que es lo que el alumno necesita para saber si puede seguir.
    """
    ej = _MANO_EJ.get(metodo)
    if ej is None:
        _display(_markdown(f'Primero ejecuta `mano_enunciado({metodo!r})`.'))
        return False

    if isinstance(valores, (int, float)):
        valores = [valores]
    try:
        vals = [float(v) for v in valores]
    except (TypeError, ValueError):
        _display(_markdown('⚠️ Reporta una **lista de números**, por ejemplo '
                           '`[1.2345, 6.7890]`.'))
        return False

    ref = catalogo.referencia(metodo, ej)
    _MANO[metodo] = vals

    if len(vals) != len(ref):
        _MANO_OK[metodo] = False
        _display(_markdown(
            f'⚠️ Reportaste **{len(vals)}** valores y hacen falta **{len(ref)}**: '
            + ', '.join(f'${etq}$' for etq, _ in ref)))
        return False

    filas = ['| valor | reportado | ¿coincide? |', '|---|---:|:---:|']
    todo = True
    for (etq, r), v in zip(ref, vals):
        ok = comun.cerca_relativa(v, r, TOL_MANO)
        todo = todo and ok
        filas.append(f'| ${etq}$ | {v:.6g} | {"✅" if ok else "❌"} |')

    _MANO_OK[metodo] = todo
    _display(_markdown('\n'.join(filas)))
    _display(_markdown('✅ **Actividad a mano correcta.**' if todo else
                       '❌ Todavía hay valores fuera de tolerancia. Revisa el '
                       'paso y no redondees a la mitad del cálculo.'))
    return todo


def mano_comprueba_todos(metodos=None):
    """Celda final: resume TODAS las actividades a mano en una tabla."""
    lista = tuple(metodos) if metodos else catalogo.METODOS
    filas = ['| # | método | estado |', '|---:|---|:---:|']
    faltan = []
    for i, metodo in enumerate(lista, start=1):
        if metodo not in _MANO_OK:
            estado = '⬜ sin comprobar'
            faltan.append(catalogo.NOMBRE_METODO[metodo])
        else:
            estado = '✅ correcta' if _MANO_OK[metodo] else '❌ con errores'
        filas.append(f'| {i} | {catalogo.NOMBRE_METODO[metodo]} | {estado} |')

    _display(_markdown('### ✅ Verificación de las actividades a mano'))
    _display(_markdown('\n'.join(filas)))
    if faltan:
        _display(_markdown('⚠️ Sin comprobar: ' + ', '.join(faltan)))
    hechas = sum(1 for m in lista if _MANO_OK.get(m))
    _display(_markdown(f'**{hechas} de {len(lista)}** correctas.'))
    return hechas, len(lista)


def mano_valores(metodo):
    """Lo que reportó el alumno (para depurar o para la hoja de trabajo)."""
    return _MANO.get(metodo)


def mano_ejercicio(metodo):
    """El ejercicio sorteado de una actividad a mano."""
    return _MANO_EJ.get(metodo)


__all__ = [
    'mano_comprueba', 'mano_comprueba_todos', 'mano_ejercicio',
    'mano_enunciado', 'mano_valores', 'TOL_MANO',
]
