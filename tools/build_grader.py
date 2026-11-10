"""build_grader.py — empaqueta un cuaderno en un blob ofuscado.

El alumno recibe UN archivo, ``grader/<cuaderno>.txt`` (base64 + zlib), con:

    - todo el framework ``lib/mn_motor/``
    - el catálogo ``preguntas/_fabrica.py``
    - las preguntas de ``preguntas/<cuaderno>/``

No es cifrado: quien sepa descomprimirlo puede leerlo. Sirve para que las
respuestas no estén a la vista de un simple vistazo. El anti-copia de verdad es
que los casos ocultos salen de la semilla del número de control.

Uso::

    python tools/build_grader.py                 # todos los cuadernos
    python tools/build_grader.py --cuaderno u4_01_interpolacion

Antes de escribir el blob comprueba, sobre el paquete REAL, que:
    1. todo compile y se cargue desde memoria (como lo hará el alumno),
    2. genere las preguntas esperadas,
    3. un alumno con las funciones de referencia saque 100.
"""
import argparse
import base64
import os
import sys
import zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MOTOR = os.path.join(RAIZ, 'lib', 'mn_motor')
PREGUNTAS = os.path.join(RAIZ, 'preguntas')

# Un cuaderno = una carpeta de preguntas = un blob = una pestaña del backend.
CUADERNOS = {
    'u4_01_interpolacion': 'U4_01_Interpolacion',
    'u4_02_newton_lagrange': 'U4_02_Newton_Lagrange',
    'u4_03_minimos_cuadrados': 'U4_03_Minimos_Cuadrados',
    'u4_04_casos': 'U4_04_Casos',
}

_COLA = '''

# =====================================================================
# Cargador generado por tools/build_grader.py
# =====================================================================
_MODULOS_PY = {modulos!r}


def _instalar(modulos):
    """Crea los módulos en memoria, sin tocar el disco ni sys.path."""
    import sys as _sys
    import types as _types

    raices = {{n.split('.')[0] for n in modulos}}
    for nombre in list(_sys.modules):
        if nombre.split('.')[0] in raices:
            del _sys.modules[nombre]

    for nombre in modulos:
        partes = nombre.split('.')
        for i in range(1, len(partes) + 1):
            parcial = '.'.join(partes[:i])
            if parcial in _sys.modules:
                continue
            modulo = _types.ModuleType(parcial)
            modulo.__path__ = []
            _sys.modules[parcial] = modulo
            if i > 1:
                setattr(_sys.modules['.'.join(partes[:i - 1])], partes[i - 1], modulo)

    pendientes = dict(modulos)
    ultimo_error = None
    while pendientes:
        progreso = False
        for nombre in list(pendientes):
            modulo = _sys.modules[nombre]
            modulo.__file__ = '<blob>/' + nombre.replace('.', '/') + '.py'
            codigo = compile(pendientes[nombre], modulo.__file__, 'exec')
            try:
                exec(codigo, modulo.__dict__)
            except ImportError as exc:
                ultimo_error = exc
                continue
            del pendientes[nombre]
            progreso = True
        if not progreso:
            raise ImportError(
                'No pude cargar el blob: ' + repr(ultimo_error) +
                ' (faltan ' + ', '.join(sorted(pendientes)) + ')')


_instalar(_MODULOS_PY)

import mn_motor.ajustes as _ajustes
_ajustes.CUADERNO = {cuaderno!r}
_ajustes.TAREA_ID = {tarea_id!r}

import mn_motor as _motor

__all__ = list(_motor.__all__)
globals().update({{nombre: getattr(_motor, nombre) for nombre in _motor.__all__}})
'''


def _leer_py(carpeta, prefijo):
    """Módulos de un paquete: {nombre_punteado: fuente}."""
    modulos = {}
    for raiz, subcarpetas, archivos in os.walk(carpeta):
        subcarpetas[:] = [d for d in subcarpetas if d != '__pycache__']
        for archivo in sorted(archivos):
            if not archivo.endswith('.py'):
                continue
            ruta = os.path.join(raiz, archivo)
            relativa = os.path.relpath(ruta, carpeta)
            partes = relativa.replace(os.sep, '/')[:-3].split('/')
            if partes[-1] == '__init__':
                partes = partes[:-1]
            nombre = '.'.join(([prefijo] + partes) if partes else [prefijo])
            with open(ruta, encoding='utf-8') as f:
                modulos[nombre] = f.read()
    return modulos


def _verificar(codigo, cuaderno, tarea_id):
    """Carga el blob en un namespace limpio y comprueba que califica bien."""
    ns = {'__name__': 'blob_prueba', '__file__': '<blob>'}
    exec(compile(codigo, '<blob>', 'exec'), ns)

    for nombre in ns['__all__']:
        if nombre not in ns:
            raise AssertionError(f'__all__ menciona {nombre!r} y no se exportó')
    if ns['cuaderno']() != cuaderno:
        raise AssertionError(f'el blob quedó apuntando a {ns["cuaderno"]()!r}')

    import mn_motor.ejercicios_u4 as cat

    tarea = ns['generar_tarea']('m16330887@hermosillo.tecnm.mx', 'Prueba')
    if not tarea['preguntas']:
        raise AssertionError('la tarea salió sin preguntas')
    if tarea['tarea'] != tarea_id:
        raise AssertionError(f'la tarea se envía como {tarea["tarea"]!r}')

    otra = ns['generar_tarea']('m99999999@hermosillo.tecnm.mx', 'Otro')
    firma = [[c[0] for c in q['casos']] for q in tarea['preguntas']]
    firma2 = [[c[0] for c in q['casos']] for q in otra['preguntas']]
    if firma == firma2:
        raise AssertionError('dos alumnos recibieron los mismos casos')

    # Alumno perfecto: las funciones de referencia del motor empaquetado.
    import importlib
    u3 = importlib.import_module('mn_motor.solvers_u3')
    u4 = importlib.import_module('mn_motor.solvers_u4')
    marco = {}
    for m in cat.METODOS:
        nombre = cat.NOMBRE_FUNCION[m]
        if hasattr(u4, nombre):
            marco[nombre] = getattr(u4, nombre)
        elif hasattr(u3, nombre):
            marco[nombre] = getattr(u3, nombre)
    puntos = 0
    for q in tarea['preguntas']:
        q['respuestas'] = None
        fn = marco.get(q['funcion'])
        if fn is None:
            raise AssertionError(f'falta la referencia de {q["funcion"]!r}')
        acierto = all(_cerca(fn(*c[0]), c[1]) for c in q['casos'])
        puntos += 1 if acierto else 0
    if puntos != len(tarea['preguntas']):
        raise AssertionError(f'el alumno perfecto sacó {puntos}/{len(tarea["preguntas"])}')

    return len(tarea['preguntas'])


def _cerca(a, b):
    """Comparación local, sin depender del motor ya cargado."""
    if isinstance(b, (list, tuple)):
        if hasattr(a, 'tolist'):
            a = a.tolist()
        return (isinstance(a, (list, tuple)) and len(a) == len(b)
                and all(_cerca(x, y) for x, y in zip(a, b)))
    try:
        return abs(float(a) - float(b)) <= 1e-6 * max(1.0, abs(float(b)))
    except (TypeError, ValueError):
        return False


def construir_blob(cuaderno, salida=None, verboso=True):
    """Empaqueta un cuaderno. Devuelve (ok, mensaje)."""
    carpeta = os.path.join(PREGUNTAS, cuaderno)
    if not os.path.isdir(carpeta):
        return False, f'no existe preguntas/{cuaderno}/'

    modulos = _leer_py(MOTOR, 'mn_motor')
    with open(os.path.join(PREGUNTAS, '__init__.py'), encoding='utf-8') as f:
        modulos['preguntas'] = f.read()
    with open(os.path.join(PREGUNTAS, '_fabrica.py'), encoding='utf-8') as f:
        modulos['preguntas._fabrica'] = f.read()
    modulos.update(_leer_py(carpeta, 'preguntas.' + cuaderno))

    if 'preguntas.' + cuaderno not in modulos:
        return False, f'falta preguntas/{cuaderno}/__init__.py'

    tarea_id = CUADERNOS[cuaderno]
    codigo = _COLA.format(modulos=modulos, cuaderno=cuaderno, tarea_id=tarea_id)

    try:
        n = _verificar(codigo, cuaderno, tarea_id)
    except Exception as exc:
        return False, f'el paquete no funciona: {exc!r}'

    blob = base64.b64encode(zlib.compress(codigo.encode('utf-8'), 9)).decode('ascii')
    destino = salida or os.path.join(RAIZ, 'grader', cuaderno + '.txt')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'w', encoding='utf-8', newline='\n') as f:
        f.write(blob)

    vuelta = zlib.decompress(base64.b64decode(blob)).decode('utf-8')
    if vuelta != codigo:
        return False, 'la descompresión no coincide'

    if verboso:
        print(f'{cuaderno}')
        print(f'  preguntas   : {n}')
        print(f'  módulos     : {len(modulos)}')
        print(f'  empaquetado : {len(codigo):,} → {len(blob):,} caracteres '
              f'({len(blob) / len(codigo):.2f}x)')
        print(f'  salida      : {os.path.relpath(destino, RAIZ)}')
    return True, destino


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cuaderno', default=None, choices=sorted(CUADERNOS))
    ap.add_argument('--salida', default=None)
    args = ap.parse_args()

    lista = [args.cuaderno] if args.cuaderno else list(CUADERNOS)
    fallos = 0
    for cuaderno in lista:
        ok, msg = construir_blob(cuaderno, args.salida)
        if not ok:
            fallos += 1
            print(f'⛔ {cuaderno}: {msg}', file=sys.stderr)
        print()
    if fallos:
        return 1
    print(f'Verificado: {len(lista)} blob(s) se descomprimen, cargan en memoria '
          f'y califican bien.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
