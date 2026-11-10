"""crear_cuadernos.py — genera los cuatro cuadernos de la Unidad 4.

Cada cuaderno repite el mismo bloque por método:

    1. Explicación del algoritmo
    2. Actividad a mano (datos sembrados por número de control)
    3. Programar la función (archivo de ``ejercicios/`` ya armado)
    4. Laboratorio con gráficas

y termina con las cuatro celdas de cierre: verificación de las actividades a
mano, verificación de las preguntas, envío y consulta del envío.

Uso::

    python tools/crear_cuadernos.py
"""

import os

import nbformat as nbf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "notebooks")

# ---------------------------------------------------------------------
# Celda 1: entorno (local o Colab) + repositorio + motor
# ---------------------------------------------------------------------
ENTORNO = r'''#@title ⚙️ Entorno — ejecuta esta celda PRIMERO
# ---------------------------------------------------------------
# En tu computadora usa los archivos locales, sin repositorio.
# En Google Colab pide UNA vez el enlace de tu fork, lo guarda en tu
# Drive y a partir de ahí lo reutiliza solo.
# ---------------------------------------------------------------
import json
import os
import subprocess
import sys

CUADERNO = {cuaderno!r}
TAREA_ID = {tarea_id!r}
REPO_NOMBRE = "U4_Repo"
GUARDADO = os.path.join("CursoMN", "u4_repo.json")   # relativo a MyDrive

try:
    import google.colab  # noqa: F401
    ES_COLAB = True
except ImportError:
    ES_COLAB = False


def _raiz_local():
    """Sube desde la carpeta actual hasta encontrar lib/robomat.py."""
    candidatos = [os.getcwd()]
    nb = globals().get("__vsc_ipynb_file__")
    if nb:
        candidatos.append(os.path.dirname(os.path.abspath(nb)))
    for base in candidatos:
        b = base
        for _ in range(6):
            if os.path.exists(os.path.join(b, "lib", "robomat.py")):
                return b
            padre = os.path.dirname(b)
            if padre == b:
                break
            b = padre
    return None


def _normaliza(enlace):
    enlace = (enlace or "").strip().rstrip("/")
    if enlace.endswith(".git"):
        enlace = enlace[:-4]
    if not enlace.startswith("https://github.com/"):
        raise ValueError("Necesito un enlace https://github.com/USUARIO/"
                         + REPO_NOMBRE + " (tu fork).")
    return enlace


if not ES_COLAB:
    REPO = _raiz_local()
    if REPO is None:
        raise RuntimeError(
            "No encontré la raíz del repositorio (lib/robomat.py).\n"
            "Abre el cuaderno dentro de U4_Repo o ejecútalo desde esa carpeta.")
    print("Modo        : local (sin repositorio)")
    print("Repositorio :", REPO)
else:
    from google.colab import drive
    drive.mount("/content/drive")
    DRIVE = "/content/drive/MyDrive"
    ruta_json = os.path.join(DRIVE, GUARDADO)

    guardado = {{}}
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, encoding="utf-8") as f:
                guardado = json.load(f)
        except Exception:
            guardado = {{}}

    enlace = (guardado.get("repo") or "").strip()
    if enlace:
        print("✅ Repositorio guardado:", enlace)
        print("   (si cambió, edita la caja de abajo y pulsa el botón)")
    else:
        try:
            enlace = input("Pega el enlace de TU fork de U4_Repo: ")
        except Exception:
            enlace = ""
        enlace = (enlace or "").strip()
        if not enlace:
            raise RuntimeError(
                "Sin repositorio no puedo continuar en Colab.\n"
                "Haz fork del repositorio del curso y pega su enlace.")

    enlace = _normaliza(enlace)
    REPO = os.path.join(DRIVE, "CursoMN", REPO_NOMBRE)

    if not os.path.exists(REPO):
        print("Clonando tu repositorio…")
        subprocess.run(["git", "clone", enlace + ".git", REPO], check=True)
    else:
        print("Actualizando tu repositorio…")
        subprocess.run(["git", "-C", REPO, "pull", "--ff-only"], check=False)

    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump({{"repo": enlace}}, f, indent=1)
    print("Repositorio :", REPO)

# --- Motor de calificación -------------------------------------------
if ES_COLAB:
    import base64
    import zlib

    ruta_blob = os.path.join(REPO, "grader", CUADERNO + ".txt")
    with open(ruta_blob, encoding="utf-8") as f:
        codigo = zlib.decompress(base64.b64decode(f.read().strip())).decode("utf-8")
    _MOTOR = {{"__name__": "mn_motor_blob", "__file__": "<blob>"}}
    exec(compile(codigo, "<blob>", "exec"), _MOTOR)
    globals().update({{n: _MOTOR[n] for n in _MOTOR["__all__"]}})
    print("Motor       : blob verificado")
else:
    _lib = os.path.join(REPO, "lib")
    if _lib not in sys.path:
        sys.path.insert(0, _lib)
    import mn_motor as _motor
    globals().update({{n: getattr(_motor, n) for n in _motor.__all__}})
    print("Motor       : módulos de lib/mn_motor")

usar_cuaderno(CUADERNO, TAREA_ID)

# --- Preludio estilo MATLAB y herramientas de gráficas ---------------
with open(os.path.join(REPO, "lib", "robomat.py"), encoding="utf-8") as f:
    exec(f.read(), globals())

if REPO not in sys.path:
    sys.path.insert(0, REPO)          # para importar ejercicios/
sys.path.append(os.path.join(REPO, "tools"))
import importlib
import visualizar
importlib.reload(visualizar)

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (9, 4.5)
plt.rcParams["figure.dpi"] = 110
print("Preludio    : lib/robomat.py · tools/visualizar.py")
print("\nListo. Ejecuta la celda de identificación.")
'''

IDENTIFICACION = r'''#@title 👤 Identificación (número de control)
# ---------------------------------------------------------------
# En Colab se toma tu correo institucional; en local se escribe uno
# de prueba. De ahí sale el número de control que siembra tus datos.
# ---------------------------------------------------------------
if ES_COLAB:
    import requests

    from google.colab import auth
    import google.auth
    import google.auth.transport.requests

    auth.authenticate_user()
    creds, _ = google.auth.default()
    creds.refresh(google.auth.transport.requests.Request())
    info = requests.get(
        "https://www.googleapis.com/drive/v3/about?fields=user",
        headers={{"Authorization": "Bearer " + creds.token}}, timeout=20).json()
    cuenta = info.get("user", {{}})
    email = cuenta.get("emailAddress", "")
    nombre = cuenta.get("displayName", "")
else:
    email = "m16330887@hermosillo.tecnm.mx"   # <-- cambia por el tuyo
    nombre = ""

if not (email and "@" in email and email.lower().endswith(".tecnm.mx")):
    from IPython.display import HTML, display
    display(HTML(
        '<p style="color:#b00020;background:#ffe0e0;padding:12px;'
        'border-radius:8px;font-weight:bold">⛔ Usa tu correo @….tecnm.mx</p>'))
    raise RuntimeError("Necesito tu correo institucional para sembrar tus datos.")

print("Alumno :", email)
print("NC     :", extraer_nc(email))
MI_TAREA = generar_tarea(email, nombre)
print("Cuaderno:", MI_TAREA["cuaderno"],
      "·", len(MI_TAREA["preguntas"]), "preguntas")
'''

CIERRE_MANO = r'''#@title ✅ 1 · Verificación de los ejercicios a mano
mano_comprueba_todos([{metodos}])
'''

CIERRE_CALIFICAR = r'''#@title 📝 2 · Verificación de todas las preguntas (no envía nada)
puntos, maximo = calificar()
'''

CIERRE_ENVIAR = r'''#@title 📤 3 · Envío de las respuestas
enviar(email)
'''

CIERRE_CONSULTAR = r'''#@title 🔎 4 · Verificación de lo que ya está enviado (no envía nada)
consultar_calificacion()
'''


def md(nb, texto):
    nb.cells.append(nbf.v4.new_markdown_cell(texto.strip()))


def code(nb, texto):
    nb.cells.append(nbf.v4.new_code_cell(texto.strip()))


def nuevo(titulo, subtitulo):
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
        "colab": {"provenance": []},
    }
    md(nb, f"# {titulo}\n\n**Métodos Numéricos · Unidad 4: Ajuste de curvas e "
            f"interpolación**\n\n{subtitulo}")
    return nb


def bloque(nb, n, metodo, titulo, teoria, archivo, args, practica=True):
    """Un método: teoría, actividad a mano, función y laboratorio."""
    md(nb, f"""
---

## Método {n} · {titulo}

{teoria}
""")
    code(nb, f'#@title ✏️ Actividad a mano · {titulo}\nEJ_{n} = mano_enunciado("{metodo}")')
    code(nb, f"""#@title ✅ Comprueba tus valores a mano · {titulo}
# Reporta los números que obtuviste, con 4 decimales.
mano_comprueba("{metodo}", [{args}])""")
    md(nb, f"""
### 💻 Programa la función

Abre `ejercicios/{archivo}` (en Codespaces) o copia la plantilla aquí abajo.
El método completo debe **llamar** a sus piezas: no repitas la cuenta.
""")
    code(nb, f"""#@title 💻 Tu función · {titulo}
from ejercicios.{archivo.replace('/', '.').replace('.py', '')} import *
""")
    if practica:
        code(nb, f'#@title ▶️ Prueba tu función con el ejemplo genérico\npractica("f_{metodo.lower()}")')
    code(nb, f'#@title 📊 Laboratorio · {titulo}\nvisualizar.laboratorio("{metodo}", EJ_{n})')


def preguntas_celda(nb, n, metodo):
    code(nb, f'#@title 🧪 Pregunta {n} · {metodo}\n# Cuando tu función ya funcione, contéstala aquí.\n'
             f'pregunta({n})')


# =====================================================================
# Cuaderno 01 — Interpolación
# =====================================================================
NB01 = [
    ("INTERP_LINEAL", "Interpolación lineal",
     r"""Es unir dos puntos con una recta. Por triángulos semejantes,

$$f_1(x)=f(x_0)+\frac{f(x_1)-f(x_0)}{x_1-x_0}(x-x_0) \tag{18.2}$$

El cociente es la pendiente y, además, una aproximación a la primera derivada.
Cuando más cerca estén los nodos, mejor representa la recta a la curva.""",
     "interpolacion/interpolacion_lineal.py", "0.0"),

    ("COEF_CUADRATICOS", "Coeficientes de la parábola",
     r"""Con tres puntos se ajusta el único polinomio de segundo grado:

$$f_2(x)=b_0+b_1(x-x_0)+b_2(x-x_0)(x-x_1) \tag{18.3}$$

donde

$$b_0=f(x_0) \tag{18.4}$$

$$b_1=\frac{f(x_1)-f(x_0)}{x_1-x_0} \tag{18.5}$$

$$b_2=\frac{\dfrac{f(x_2)-f(x_1)}{x_2-x_1}-\dfrac{f(x_1)-f(x_0)}{x_1-x_0}}{x_2-x_0} \tag{18.6}$$

Los dos primeros términos son la recta; $b_2$ aporta la curvatura.""",
     "interpolacion/coeficientes_cuadraticos.py", "0.0, 0.0"),

    ("INTERP_CUADRATICA", "Interpolación cuadrática",
     r"""Ya con $b_0, b_1, b_2$ se evalúa (18.3) en el punto pedido. Esta
función **debe llamar** a `coeficientes_cuadraticos`: la pieza y el método no
se programan dos veces.""",
     "interpolacion/interpolacion_cuadratica.py", "0.0"),

    ("ERROR_INTERP", "Error con un punto extra",
     r"""Si se tiene un nodo más de lo necesario, se estima el error:

$$R_n\cong f[x_{n+1},x_n,\dots,x_0]\prod_{i=0}^{n}(x-x_i) \tag{18.18}$$

Es la diferencia entre la predicción de grado $n+1$ y la de grado $n$.""",
     "interpolacion/error_estimado_interpolacion.py", "0.0"),
]

# ======================================================================
# Cuaderno 02 — Newton y Lagrange
# ======================================================================
NB02 = [
    ("NEWTON_TABLA", "Tabla de diferencias divididas",
     r"""La primera diferencia dividida es una pendiente,

$$f[x_i,x_j]=\frac{f(x_i)-f(x_j)}{x_i-x_j} \tag{18.12}$$

y las siguientes se construyen con las anteriores:

$$f[x_i,x_j,x_k]=\frac{f[x_i,x_j]-f[x_j,x_k]}{x_i-x_k} \tag{18.13}$$

La tabla es triangular y su **diagonal** son los coeficientes del polinomio.""",
     "newton_lagrange/tabla_diferencias.py", "0.0, 0.0, 0.0, 0.0"),

    ("NEWTON_EVAL", "Polinomio de Newton en diferencias divididas",
     r"""La forma general agrega un término por nodo:

$$f_n(x)=b_0+b_1(x-x_0)+\cdots+b_n(x-x_0)\cdots(x-x_{n-1}) \tag{18.7}$$

Se evalúa con Horner: $p=b_n$ y luego $p\leftarrow p(x-x_k)+b_k$. Esta función
**debe llamar** a `coeficientes_newton` y a `evaluar_newton`.""",
     "newton_lagrange/interpolacion_newton.py", "0.0"),

    ("LAGRANGE", "Polinomio de Lagrange",
     r"""Es una reformulación que evita las diferencias divididas:

$$f_n(x)=\sum_{i=0}^{n}L_i(x)f(x_i),\qquad
L_i(x)=\prod_{\substack{j=0\\ j\neq i}}^{n}\frac{x-x_j}{x_i-x_j} \tag{18.20–18.21}$$

Cada peso vale 1 en su nodo y 0 en los demás. Da **el mismo** polinomio que
Newton.""",
     "newton_lagrange/interpolacion_lagrange.py", "0.0"),

    ("ERROR_NEWTON", "Error del polinomio",
     r"""El término que se agrega al subir de grado es una estimación del error
de grado $n$:

$$R_n=f_{n+1}(x)-f_n(x)=b_n\prod_{i<n}(x-x_i) \tag{18.19}$$""",
     "newton_lagrange/error_newton.py", "0.0"),
]

# ======================================================================
# Cuaderno 03 — Mínimos cuadrados
# ======================================================================
NB03 = [
    ("SUMA_RESIDUOS", "Suma de residuos al cuadrado",
     r"""El criterio de mínimos cuadrados es minimizar

$$S_r=\sum_{i=1}^{n}e_i^2=\sum_{i=1}^{n}\left(y_i-a_0-a_1x_i-\cdots\right)^2 \tag{17.3}$$

Se usan cuadrados para que los errores no se cancelen y el mínimo sea único.""",
     "minimos_cuadrados/suma_residuos_cuadrados.py", "0.0"),

    ("REG_LINEAL", "Regresión lineal",
     r"""Al derivar (17.3) e igualar a cero salen las **ecuaciones normales**:

$$n a_0+\left(\sum x_i\right)a_1=\sum y_i \tag{17.4}$$

$$\left(\sum x_i\right)a_0+\left(\sum x_i^2\right)a_1=\sum x_i y_i \tag{17.5}$$

y su solución,

$$a_1=\frac{n\sum x_iy_i-\sum x_i\sum y_i}{n\sum x_i^2-\left(\sum x_i\right)^2},\qquad
a_0=\bar y-a_1\bar x \tag{17.6–17.7}$$
""",
     "minimos_cuadrados/regresion_lineal.py", "0.0, 0.0, 0.0"),

    ("REG_CUADRATICA", "Regresión cuadrática",
     r"""Para $y=a_0+a_1x+a_2x^2$ las ecuaciones normales son un sistema $3\times3$:

$$\begin{bmatrix}n&\sum x_i&\sum x_i^2\\ \sum x_i&\sum x_i^2&\sum x_i^3\\ \sum x_i^2&\sum x_i^3&\sum x_i^4\end{bmatrix}
\begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}=\begin{bmatrix}\sum y_i\\ \sum x_iy_i\\ \sum x_i^2y_i\end{bmatrix} \tag{17.19}$$

Resolverlo es resolver un sistema lineal: aquí se ve por qué sirve el capítulo 3.""",
     "minimos_cuadrados/regresion_cuadratica.py", "0.0, 0.0, 0.0, 0.0"),

    ("ERROR_ESTANDAR", "Error estándar de la estimación",
     r"""Mide la dispersión alrededor del modelo, no alrededor de la media:

$$s_{y/x}=\sqrt{\frac{S_r}{n-(m+1)}} \tag{17.9, 17.20}$$

Se pierden $m+1$ grados de libertad porque se estimaron $m+1$ coeficientes.""",
     "minimos_cuadrados/error_estandar.py", "0.0"),

    ("COEF_DETERMINACION", "Coeficiente de determinación",
     r"""Cuánto de la incertidumbre original explica el modelo:

$$r^2=\frac{S_t-S_r}{S_t} \tag{17.10}$$

Un $r^2$ cercano a 1 **no** prueba que la forma sea la correcta: hay que
graficar.""",
     "minimos_cuadrados/coeficiente_determinacion.py", "0.0"),
]

# ======================================================================
# Cuaderno 04 — Casos (U3 + U4) y Fourier extra
# ======================================================================
NB04 = [
    ("FOURIER", "Serie de Fourier (tarea extra)",
     r"""Con datos igualmente espaciados que completan un periodo, los
coeficientes salen de sumas simples:

$$A_0=\frac{\sum y}{N},\qquad
A_j=\frac{2}{N}\sum y\cos(j\omega_0t),\qquad
B_j=\frac{2}{N}\sum y\operatorname{sen}(j\omega_0t) \tag{19.14–19.16}$$

El modelo es lineal en $A_j$ y $B_j$, así que es mínimos cuadrados con otra
base de funciones.""",
     "casos/coeficientes_fourier.py", "0.0, 0.0, 0.0"),
]


def construir(nb, metodos, prefijo):
    for n, (metodo, titulo, teoria, archivo, args) in enumerate(metodos, start=1):
        bloque(nb, n, metodo, titulo, teoria, archivo, args)
        preguntas_celda(nb, n, titulo)
    return nb


CASOS_U3_U4 = r'''
---

## Caso A · Calibración de un sensor (mínimos cuadrados + sistemas lineales)

**El problema.** Un sensor entrega una lectura digital $x$ y se calibra contra
un patrón de temperatura $y$. El fabricante reporta ruido de $\pm0.1$ °C.

| $x$ (cuentas) | 0 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|
| $y$ (°C) | 0.2 | 0.9 | 1.8 | 2.5 | 3.4 | 4.2 | 5.4 | 6.2 | 7.5 | 8.4 |

**¿Interpolar o ajustar?** Ajustar: hay 10 mediciones con ruido. Interpolar con
grado 9 copiaría el ruido.

**El método más efectivo aquí** es mínimos cuadrados **cuadráticos** (17.19),
porque el lineal deja estructura en los residuales. Y hay un detalle que
conecta las dos unidades: las ecuaciones normales **son un sistema lineal**, así
que se resuelven con lo de la Unidad 3.

**Otros métodos viables.** Lineal (más simple, deja curvatura); cúbico (no
mejora y no se justifica); interpolación (sobreajuste).
'''

CASO_A_CODIGO = r'''#@title 🧩 Caso A · ecuaciones normales resueltas con Gauss (Unidad 3)
from ajuste_curvas import minimos_cuadrados

x_s = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90], dtype=float)
y_s = np.array([0.2, 0.9, 1.8, 2.5, 3.4, 4.2, 5.4, 6.2, 7.5, 8.4])


def gauss_solve(A, b):
    """Eliminación gaussiana con sustitución hacia atrás (Unidad 3)."""
    A = np.array(A, dtype=float).copy()
    b = np.array(b, dtype=float).copy()
    n = len(b)
    for k in range(n - 1):
        if A[k, k] == 0:
            raise ZeroDivisionError(f"pivote cero en la columna {k + 1}")
        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x


n_s = len(x_s)
A_norm = np.array([[n_s, x_s.sum(), (x_s ** 2).sum()],
                   [x_s.sum(), (x_s ** 2).sum(), (x_s ** 3).sum()],
                   [(x_s ** 2).sum(), (x_s ** 3).sum(), (x_s ** 4).sum()]])
b_norm = np.array([y_s.sum(), (x_s * y_s).sum(), (x_s ** 2 * y_s).sum()])

coef_gauss = gauss_solve(A_norm, b_norm)
coef_lib = minimos_cuadrados(x_s, y_s, 2)["coef"]
print("con Gauss (U3) :", np.round(coef_gauss, 6))
print("con la librería:", np.round(coef_lib, 6))
print("¿coinciden?     :", np.allclose(coef_gauss, coef_lib, atol=1e-9))
'''

CASO_A_CIERRE = r'''#@title 🧩 Caso A · ¿lineal o cuadrático? la evidencia
for m in (1, 2):
    r = minimos_cuadrados(x_s, y_s, m)
    print(f"grado {m}: sy/x = {r['syx']:.4f} °C · r2 = {r['r2']:.5f}")

print("\nruido del sensor = 0.1 °C")
print("El lineal queda por encima del ruido y deja curvatura;")
print("el cuadrático baja al orden del ruido: se justifica el término x^2.")
'''


def casos(nb):
    md(nb, CASOS_U3_U4)
    code(nb, CASO_A_CODIGO)
    code(nb, CASO_A_CIERRE)


def cierres(nb, metodos):
    code(nb, CIERRE_MANO.format(
        metodos=", ".join(f'"{m[0]}"' for m in metodos)))
    code(nb, CIERRE_CALIFICAR)
    code(nb, CIERRE_ENVIAR)
    code(nb, CIERRE_CONSULTAR)
    return nb


def main():
    os.makedirs(SALIDA, exist_ok=True)

    especificaciones = [
        ("U4_01_Interpolacion.ipynb", "u4_01_interpolacion",
         "U4_01_Interpolacion", "📐 Cuaderno 01 — Interpolación",
         "Tema 4.1. Cada método sigue el mismo camino: **explicación → a mano → "
         "programar → laboratorio**.",
         NB01, False),
        ("U4_02_Newton_Lagrange.ipynb", "u4_02_newton_lagrange",
         "U4_02_Newton_Lagrange", "🌳 Cuaderno 02 — Newton y Lagrange",
         "Tema 4.2. Dos formas del **mismo** polinomio, más la estimación del "
         "error.",
         NB02, False),
        ("U4_03_Minimos_Cuadrados.ipynb", "u4_03_minimos_cuadrados",
         "U4_03_Minimos_Cuadrados", "📉 Cuaderno 03 — Mínimos cuadrados",
         "Tema 4.3. Cuando los datos traen ruido no se interpola: se ajusta.",
         NB03, False),
        ("U4_04_Casos.ipynb", "u4_04_casos", "U4_04_Casos",
         "🧩 Cuaderno 04 — Casos (Unidades 3 y 4)",
         "Tema 4.4. Casos que combinan **sistemas lineales** (Unidad 3) con "
         "**ajuste de curvas** (Unidad 4), y la serie de Fourier como tarea "
         "extra.",
         NB04, True),
    ]

    for archivo, cuaderno, tarea_id, titulo, subtitulo, metodos, con_casos in especificaciones:
        nb = nuevo(titulo, subtitulo)
        code(nb, ENTORNO.format(cuaderno=cuaderno, tarea_id=tarea_id))
        code(nb, IDENTIFICACION)
        if con_casos:
            casos(nb)
        construir(nb, metodos, cuaderno)
        cierres(nb, metodos)
        nbf.write(nb, os.path.join(SALIDA, archivo))
        print("escrito:", archivo, f"({len(nb.cells)} celdas)")


if __name__ == "__main__":
    main()
