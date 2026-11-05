# AP1 — Trayectoria de un robot móvil

| ⬅️ Índice de aplicaciones | 🏠 Inicio |
|:---|:---:|
| [Aplicaciones](aplicaciones_index.md) | [README](../../README.md) |

> **Tipo:** aplicación propuesta (extensión). La interpolación y la regresión
> usadas son contenido del libro; el caso del robot es nuestro.

## 1. Problema

Un robot móvil debe recorrer una planta pasando por una secuencia de puntos
(waypoints) registrados por un operador. El controlador sólo entiende
**posiciones en función del tiempo**, no una lista de puntos. Necesitamos:

1. una curva $x(t),\ y(t)$ que pase por los waypoints;
2. una estimación de la velocidad para verificar que no se excede el límite;
3. un criterio para decidir si conviene interpolar o suavizar.

## 2. Datos

| $t$ (s) | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $x$ (m) | 0.0 | 1.2 | 2.1 | 3.4 | 4.8 | 6.0 |
| $y$ (m) | 0.0 | 0.8 | 1.9 | 2.0 | 1.4 | 0.6 |

Los datos son **exactos** (los fija el operador), así que en principio se
interpola. Pero si los waypoints vinieran de un GPS con error, interpolar
reproduciría el ruido y convendría ajustar.

## 3. Solución con interpolación

**📘 Del libro.** Se aplica el polinomio de Newton (18.7) por separado a $x(t)$
e $y(t)$, tratando $t$ como la variable independiente. Como los tiempos están
igualmente espaciados, también se puede usar la forma de Lagrange (18.20);
ambas deben dar el mismo resultado.

1. Construir la tabla de diferencias divididas para $x$ y para $y$.
2. Evaluar en una malla fina $t\in[0,5]$ para dibujar la trayectoria.
3. Verificar que la curva pasa por los seis waypoints.

**Parámetro de riesgo.** El polinomio de grado 5 puede oscilar entre puntos
(el libro advierte sobre el mal condicionamiento de grados altos). Hay que
graficar y revisar.

## 4. Velocidad

**🧮 Extensión.** La velocidad se estima derivando el polinomio. Para la forma
de Newton,

$$f_n'(x)=b_1+b_2\left[(x-x_1)+(x-x_0)\right]+\cdots$$

o, más simple y suficientemente preciso para el reporte, con diferencias
finitas centrales sobre la malla:

$$v(t_i)\approx\frac{\lVert \mathbf{p}(t_{i+1})-\mathbf{p}(t_{i-1})\rVert}{t_{i+1}-t_{i-1}}.$$

Si $v_{\max}$ supera el límite del robot, hay que **rediseñar los waypoints**,
no cambiar el método de interpolación.

## 5. Variante con datos ruidosos

**🧮 Extensión.** Si se agrega ruido gaussiano a $x$ e $y$, la interpolación
pasa por los puntos ruidosos y produce una trayectoria irregular. La
alternativa es ajustar un polinomio de grado 2 o 3 por mínimos cuadrados
(17.19):

- el modelo **no** pasa por los waypoints, pero la trayectoria es suave;
- se reporta $s_{y/x}$ y $r^2$ para justificar el grado;
- se comparan ambas curvas y se discute cuál es aceptable para el robot.

## 6. Verificación

| Comprobación | Criterio |
|---|---|
| Interpolación pasa por los nodos | error $<10^{-10}$ m |
| Newton y Lagrange coinciden | diferencia $<10^{-9}$ m |
| Velocidad máxima | comparar contra el límite declarado |
| Ajuste con ruido | $s_{y/x}$ menor que la dispersión de los datos |

## 7. Qué se aprende

- La interpolación es la herramienta correcta para **datos exactos**.
- Con ruido, el criterio cambia: mínimos cuadrados, aunque no pase por los
  puntos.
- El resultado numérico no decide solo: hay una restricción física (velocidad,
  curvatura) que manda.
