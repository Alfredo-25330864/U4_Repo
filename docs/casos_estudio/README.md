# Casos de estudio — Unidad 4

| 🏠 Inicio |
|:---:|
| [README](../../README.md) |

Cada caso sigue **el mismo formato** para que el alumno no tenga que adivinar
qué se espera de él:

1. **El problema** — datos, figura y pregunta de ingeniería.
2. **¿Interpolar o ajustar?** — la decisión, con su justificación.
3. **Método recomendado** — el más efectivo para *este* problema y por qué.
4. **Otros métodos viables** — cuándo sí convienen y cuál es su costo.
5. **Código** — la llamada concreta a la función del método.
6. **Comparación con la librería** — SciPy/NumPy equivalente, si existe.
7. **Verificación** — residuales, error o comprobación física.
8. **Figura** — la misma que resume el caso.

## Índice

| Caso | Problema | Método recomendado | Librería comparada |
|---|---|---|---|
| [01](caso01_interpolacion_ln2.md) | Estimar $\ln 2$ con pocos datos | Newton cúbico | `BarycentricInterpolator`, `np.polyfit` |
| [02](caso02_robot_trayectoria.md) | Trayectoria de un robot móvil | Trazador cúbico (`CubicSpline`) | Newton grado 5, mínimos cuadrados |
| [03](caso03_sensor_regresion.md) | Calibración de un sensor | Mínimos cuadrados cuadráticos | `np.polyfit` |
| [04](caso04_fourier_lineas.md) | Imagen de líneas | Serie de Fourier con $m=5$ | `np.fft.rfft` |

## Regla de honestidad

El método recomendado **no siempre es el del libro**. Cuando la librería ofrece
algo mejor para el problema real (por ejemplo, un trazador cúbico para una
trayectoria), el caso lo dice y explica por qué. El método del libro se sigue
mostrando porque es el que se evalúa y el que enseña el mecanismo.

## Figuras

Las figuras se generan con `tools/generar_figuras.py`. No se editan a mano:
si cambian los datos, se vuelve a correr el script.
