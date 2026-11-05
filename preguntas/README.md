# Preguntas de U4 — contrato para el futuro grader

Este árbol sigue el mismo patrón que `U3_Repo` en su rama `test`. Está vacío
a propósito: primero se crea el motor (`lib/mn_motor/`) y después las preguntas.

## Estructura

```text
preguntas/
├── __init__.py
├── u4_01_interpolacion/
│   ├── __init__.py          # PREGUNTAS = [p01, p02, ...]
│   ├── p01_lineal.md        # opción múltiple
│   └── p02_newton.py        # programar / numérica / matriz
└── u4_02_newton_lagrange/
```

## Contrato de cada pregunta

Cada archivo `.py` define un objeto con un método `construir(semilla)` que
devuelve un diccionario con:

| Campo | Tipos | Descripción |
|---|---|---|
| `tipo` | `mcq`, `numero`, `matriz`, `funcion` | Cómo se califica |
| `id` | `str` | Identificador único |
| `titulo` | `str` | Título corto |
| `enunciado` | `str` | Texto con LaTeX |
| `esperado` | según tipo | Respuesta correcta (no se muestra) |
| `opciones` | `list[str]` | Sólo `mcq` |
| `funcion` | `str` | Sólo `funcion`: nombre de la función del alumno |
| `casos` | `list[(args, esperado)]` | Sólo `funcion`: casos ocultos |
| `ejemplo` | `(args, esperado)` | Sólo `funcion`: ejemplo visible |
| `referencia` | `str` | Sólo `funcion`: nombre en `solvers_u4` |
| `ayuda` | `str` | Opcional |

Las preguntas de opción múltiple se escriben en `.md` y se declaran con
`mn_motor.mcq.desde_markdown('preguntas/.../p01.md')`.

## Referencias numéricas

`lib/mn_motor/solvers_u4.py` contiene las implementaciones de referencia
(Newton, Lagrange, mínimos cuadrados, Fourier y la parábola de optimización).
Se usan con `referencia='newton'`, `referencia='minimos_cuadrados'`, etc.

## Regla de oro

La respuesta correcta **nunca** se calcula en el cuaderno del alumno: se
calcula en el motor y se compara contra lo que el alumno respondió.
