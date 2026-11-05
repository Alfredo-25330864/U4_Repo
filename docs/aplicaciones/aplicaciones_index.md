# Aplicaciones de la Unidad 4

| 🏠 Inicio |
|:---:|
| [README](../../README.md) |

> Las tres aplicaciones usan las funciones de `lib/ajuste_curvas.py` y se
> resuelven en el cuaderno `U4_04_Aplicaciones.ipynb`. Cada ficha separa
> **lo que viene del libro** de la **extensión propuesta**.

## 📑 Índice

1. [Trayectoria de un robot móvil](ap1_trayectoria_robot.md) — interpolación
   de waypoints y suavizado por mínimos cuadrados.
2. [Imagen de líneas con series de Fourier](ap2_fourier_lineas_imagen.md) —
   perfil de una imagen, ajuste sinusoidal y reconstrucción.
3. [Calibración de un sensor](ap3_calibracion_sensor.md) — elección entre
   modelo lineal y cuadrático con $s_{y/x}$ y $r^2$.

## 🧭 Cómo se relacionan con el programa

| Aplicación | Temas | Herramientas |
|---|---|---|
| Robot móvil | 4.1, 4.2, 4.3 | Newton, Lagrange, mínimos cuadrados |
| Fourier | 4.3, 4.4 | Ecuaciones normales (19.12), DFT |
| Sensor | 4.3, 4.4 | Ecuaciones normales, $s_{y/x}$, $r^2$ |

## ⚖️ Criterio de inclusión

Una aplicación entra a la unidad sólo si:

1. se puede implementar con las funciones de la unidad;
2. obliga a **decidir** entre interpolar y ajustar;
3. tiene una verificación numérica clara (residual, reconstrucción o
   comparación contra un valor conocido).

Las tres cumplen. La optimización con interpolación parabólica (capítulo 4,
sección 13.2) queda como puente conceptual en
[la comparativa](../metodos/05_comparativa_interpolacion_regresion.md#sec-4) y
como práctica en el cuaderno 04.
