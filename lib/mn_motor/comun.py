"""Utilidades compartidas por las preguntas. Nada aquí sabe de una pregunta concreta.

Si algo solo lo usa UNA pregunta, va en el archivo de esa pregunta: así el
archivo se puede auditar solo, sin saltar a otro lado.
"""
import ast
import hashlib
import re
from string import ascii_lowercase


# ---------------------------------------------------------------------
# Identificación del alumno
# ---------------------------------------------------------------------

def extraer_nc(identificador):
    """Número de Control a partir del correo institucional.

        'm16330887@hermosillo.tecnm.mx' -> '16330887'
        '16330887@hermosillo.tecnm.mx'  -> '16330887'
        'm{16330887}@tecnm.mx'          -> '16330887'
    """
    if identificador is None:
        return None
    s = str(identificador).strip()
    entre_llaves = re.search(r'\{([^}]+)\}', s)
    if entre_llaves:
        return entre_llaves.group(1).strip()
    local = s.split('@')[0]
    digitos = re.search(r'\d{4,}', local)
    return digitos.group(0) if digitos else None


def semilla_de(identificador):
    """Semilla determinista del NC: el mismo alumno recibe siempre lo mismo."""
    nc = extraer_nc(identificador) or str(identificador)
    return int(hashlib.sha256(nc.encode('utf-8')).hexdigest()[:8], 16)


def rng_de(identificador, sal=0):
    """Generador reproducible del alumno, con un desplazamiento por uso.

    ``sal`` separa los sorteos de un mismo alumno (actividad a mano, casos
    ocultos de cada pregunta, laboratorio) para que dos usos no reciban los
    mismos números por casualidad.
    """
    import numpy as np
    return np.random.default_rng(semilla_de(identificador) ^ (sal or 0))


def semilla_pregunta(identificador, sal):
    """Semilla independiente por pregunta.

    El sal es una constante distinta en cada archivo de pregunta, de modo que
    dos preguntas no reciben por casualidad los mismos números y una no puede
    delatar la respuesta de otra.
    """
    return semilla_de(identificador) ^ sal


# ---------------------------------------------------------------------
# Presentación en LaTeX
# ---------------------------------------------------------------------

def tex(matriz):
    """Matriz -> LaTeX de un bmatrix, SIN los delimitadores ``$``.

    Los ``$`` los pone quien llama, porque a veces va en línea (``$...$``) y a
    veces en su propio renglón (``$$...$$``).
    """
    filas = r' \\ '.join(
        ' & '.join(f'{v:g}' if isinstance(v, (int, float)) else str(v) for v in fila)
        for fila in matriz)
    return r'\begin{bmatrix}' + filas + r'\end{bmatrix}'


def tex_vector(valores):
    """Columna a partir de una lista plana, en LaTeX sin ``$``."""
    return tex([[v] for v in valores])


def letra(n):
    """0 -> 'a', 1 -> 'b', ..."""
    return ascii_lowercase[n]


def letras(n):
    """0..n -> 'abcd' (para marcar las opciones de opción múltiple)."""
    return ascii_lowercase[:n]


# ---------------------------------------------------------------------
# Comparar respuestas
# ---------------------------------------------------------------------

def a_lista(texto):
    """Texto del alumno -> lista de listas. Seguro: no usa ``eval``.

    Acepta también matrices (ndarray, sympy Matrix o MatrizRobomat), que es lo
    que devuelven las funciones que programan los alumnos: ``str(Matrix(...))``
    no es evaluable por ``literal_eval``, así que hay que convertirlas antes.
    """
    if texto is None:
        return None
    if hasattr(texto, 'tolist') and not isinstance(texto, (list, tuple)):
        v = texto.tolist()
        if isinstance(v, (int, float)):
            return [[v]]
        if v and isinstance(v[0], (list, tuple)):
            return [list(f) for f in v]
        return [list(v)]
    if isinstance(texto, (list, tuple)):
        return [list(f) if isinstance(f, (list, tuple)) else [f] for f in texto]
    s = str(texto).strip()
    if not s:
        return None
    try:
        v = ast.literal_eval(s)
    except Exception:
        return None
    if isinstance(v, (int, float)):
        return [[v]]
    if isinstance(v, (list, tuple)):
        if v and isinstance(v[0], (list, tuple)):
            return [list(f) for f in v]
        return [list(v)]
    return None


def matriz_igual(respuesta, esperado, tol=1e-6):
    """¿La respuesta del alumno coincide con la matriz esperada?"""
    r = a_lista(respuesta)
    if r is None:
        return False
    if len(r) != len(esperado):
        return False
    if any(len(f) != len(esperado[i]) for i, f in enumerate(r)):
        return False
    for i, fila in enumerate(r):
        for j, v in enumerate(fila):
            try:
                # Se compara al revés a propósito: con `>` un NaN pasaría,
                # porque `nan > tol` es False y el bucle seguiría.
                if not abs(float(v) - float(esperado[i][j])) <= tol:
                    return False
            except (TypeError, ValueError):
                return False
    return True


def _es_lista_de_matrices(x):
    """¿Es una tupla/lista de matrices (y no una sola matriz)?

    Una matriz es ``[[...], [...]]``: dos niveles. Una lista de matrices tiene
    tres, porque el primer elemento ya es ``[[...], ...]``.
    """
    if not isinstance(x, (list, tuple)) or not x:
        return False
    primero = x[0]
    return (isinstance(primero, (list, tuple)) and bool(primero)
            and isinstance(primero[0], (list, tuple)))


def _es_escalar(x):
    """¿Es un número suelto (y no una matriz, vector o lista)?"""
    if isinstance(x, (list, tuple)):
        return False
    if hasattr(x, 'tolist') or hasattr(x, 'rows'):
        return False
    try:
        float(x)
    except (TypeError, ValueError):
        return False
    return True


def _comparar_estructura(a, e, tol):
    """Compara recursivamente números, listas, tuplas, matrices y ``None``."""
    if e is None:
        # ``None`` significa "no aplica" (por ejemplo, un error que no se pidió).
        return a is None
    if isinstance(e, (list, tuple)):
        if hasattr(a, 'tolist') and not isinstance(a, (list, tuple)):
            a = a.tolist()
        if not isinstance(a, (list, tuple)) or len(a) != len(e):
            return False
        return all(_comparar_estructura(x, y, tol) for x, y in zip(a, e))
    return numero_igual(a, e, tol)


def comparar(respuesta, esperado, tol=1e-6):
    """Compara la respuesta con lo esperado, admitiendo escalares y listas.

    Acepta una matriz de NumPy, una lista de listas, una tupla de resultados o
    un número suelto: se compara el VALOR, no el tipo. Los métodos que
    devuelven varias piezas (``L`` y ``U``, o ``A0``, ``A`` y ``B``) se
    comparan elemento por elemento.
    """
    if isinstance(respuesta, str):
        parsed = a_lista(respuesta)
        if parsed is None:
            return False
        respuesta = parsed[0] if len(parsed) == 1 else parsed
    return _comparar_estructura(respuesta, esperado, tol)


def numero_igual(respuesta, esperado, tol=1e-6):
    try:
        return abs(float(respuesta) - float(esperado)) < tol
    except (TypeError, ValueError):
        return False


def cerca_relativa(valor, ref, tol=1e-4):
    """¿``valor`` coincide con ``ref``? Tolerancia relativa, tolerante al truncado.

    Se usa en las actividades a mano: el alumno reporta 4 decimales, así que
    truncar o redondear deben dar lo mismo. El divisor es el mayor de los dos
    (o 1), para que reportar 0 no produzca un error enorme.
    """
    try:
        v, r = float(valor), float(ref)
    except (TypeError, ValueError):
        return False
    if v != v or r != r:
        return False
    escala = max(1.0, abs(v), abs(r))
    return abs(v - r) / escala <= tol
