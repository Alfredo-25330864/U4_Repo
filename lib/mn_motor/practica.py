"""Práctica libre: prueba TU función contra un ejemplo del enunciado.

No es la calificación: aquí no hay puntos ni intentos. Sirve para que el alumno
sepa si su método ya funciona antes de enviar.

Se puede llamar de dos formas:

    practica('f_interp_lineal')     # por id de pregunta de programar
    practica('INTERP_LINEAL')       # por nombre de método del catálogo

La segunda forma no necesita que el cuaderno tenga preguntas de programar: el
ejemplo sale de ``preguntas/_fabrica.ejemplo_de``.

La referencia se calcula aquí dentro y **no se muestra**: solo el veredicto.
"""
import inspect

import mn_motor.califica as califica
import mn_motor.comun as comun
import mn_motor.ejercicios_u4 as catalogo
import mn_motor.tarea as tarea


def _resolver(id_o_metodo, t):
    """Devuelve ``(nombre_funcion, entrada, esperado, firma)`` o ``None``."""
    q = next((x for x in t['preguntas'] if x['id'] == id_o_metodo), None)
    if q is not None:
        if q['tipo'] != 'funcion':
            print(f'⚠️ La pregunta {id_o_metodo!r} no es de programar.')
            return None
        return q['funcion'], q['ejemplo'][0], q['ejemplo'][1], q.get('firma', '')

    clave = str(id_o_metodo).upper()
    if clave not in catalogo.METODOS:
        print(f'⚠️ No hay ninguna pregunta ni método con id {id_o_metodo!r}.')
        return None

    from preguntas._fabrica import ejemplo_de

    entrada, esperado = ejemplo_de(clave)
    return catalogo.NOMBRE_FUNCION[clave], entrada, esperado, ''


def practica(id_o_metodo, tarea_=None):
    """Prueba la función del alumno con un ejemplo y devuelve True/False.

    Devuelve ``None`` si falta algo (la función, el método o el marco).
    """
    t = tarea_ if tarea_ is not None else tarea.tarea_activa()
    resuelto = _resolver(id_o_metodo, t)
    if resuelto is None:
        return None
    nombre_fn, entrada, esperado, firma = resuelto

    marco_de_arriba = inspect.currentframe()
    if marco_de_arriba is None or marco_de_arriba.f_back is None:
        print('⚠️ No pude leer las variables del cuaderno; ejecuta esto desde Colab.')
        return None
    fn = califica.funcion_del_alumno(marco_de_arriba.f_back.f_globals, nombre_fn)
    if fn is None:
        print(f'⚠️ Todavía no defines tu función `{nombre_fn}`. '
              f'Escríbela arriba y vuelve a ejecutar esta celda.')
        return None

    print(f'Probando `{nombre_fn}` con un ejemplo…')
    if firma:
        print(f'   firma: {firma}')
    try:
        res = fn(*entrada)
    except NotImplementedError as exc:
        print(f'⏳ Tu función todavía tiene `raise NotImplementedError` ({exc}).')
        return False
    except Exception as exc:
        print(f'⛔ Tu función lanzó {type(exc).__name__}: {exc}')
        return False

    if res is None:
        print('⏳ Tu función devolvió `None`: todavía no calcula nada.')
        return False

    if comun.comparar(res, esperado):
        print('✅ Coincide con la referencia.')
        _mostrar(res)
        return True

    print('❌ Todavía no coincide. Tu resultado:')
    _mostrar(res)
    if isinstance(esperado, (list, tuple)):
        print(f'   Debe devolver {len(esperado)} valores; revisa el orden '
              '(primero el valor interpolado y luego el error).')
    print('   Contrasta con el pseudocódigo y con los índices '
          '(Python empieza en 0, el libro en 1).')
    return False


def _mostrar(valor):
    """Pinta el resultado del alumno, sin revelar la referencia."""
    if valor is None:
        print('   None')
        return
    if isinstance(valor, (list, tuple)):
        print('   (' + ', '.join('None' if v is None else f'{float(v):.6g}'
                                 for v in valor) + ')')
        return
    print(f'   {valor}')
