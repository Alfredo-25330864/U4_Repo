# AP3 — Calibración de un sensor

| ⬅️ Índice de aplicaciones | 🏠 Inicio |
|:---|:---:|
| [Aplicaciones](aplicaciones_index.md) | [README](../../README.md) |

> **Tipo:** aplicación propuesta (extensión). El procedimiento de mínimos
> cuadrados y las métricas $s_{y/x}$ y $r^2$ son contenido del libro
> (sección 17.1–17.2); el caso del sensor es nuestro.

## 1. Problema

Un sensor entrega una lectura digital $x$ y se calibra contra un patrón que da
la variable física $y$. Se tienen 10 pares de laboratorio. Hay que decidir
entre:

- **modelo lineal**: $y=a_0+a_1x$ (ecuaciones 17.4–17.7);
- **modelo cuadrático**: $y=a_0+a_1x+a_2x^2$ (ecuaciones 17.19).

La decisión no se toma por costumbre ni por $r^2$: se toma comparando el error
estándar y verificando que el modelo no empiece a seguir el ruido.

## 2. Datos de laboratorio

| $x$ (cuentas) | 0 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|
| $y$ (°C) | 0.2 | 0.9 | 1.8 | 2.5 | 3.4 | 4.2 | 5.4 | 6.2 | 7.5 | 8.4 |

La relación parece lineal con una ligera curvatura. El sensor tiene ruido de
$\pm0.1$ °C.

## 3. Procedimiento

1. **Graficar** $x$ contra $y$ y los residuales de cada modelo.
2. Ajustar grado 1 y grado 2 con `minimos_cuadrados`.
3. Reportar para cada modelo:

   $$s_{y/x}=\sqrt{\frac{S_r}{n-(m+1)}},\qquad
   r^2=\frac{S_t-S_r}{S_t}.$$

4. Comparar $s_{y/x}$ con el ruido del sensor ($0.1$ °C). Un modelo con
   $s_{y/x}$ muy por debajo del ruido está sobreajustando.
5. Elegir el modelo **más simple** cuyo $s_{y/x}$ sea comparable al ruido.
6. Reportar la ecuación de calibración con sus unidades.

## 4. Verificación

| Comprobación | Criterio |
|---|---|
| Residual medio | $\approx0$ |
| $s_{y/x}$ | del orden del ruido del sensor |
| Coeficientes | estables al quitar un punto (validación cruzada simple) |
| $r^2$ | alto, pero no usado como único criterio |

**🧮 Prueba de estabilidad.** Se repite el ajuste dejando fuera un punto y se
observa cuánto cambian los coeficientes. Si el modelo cuadrático cambia mucho
y el lineal no, el término $x^2$ no está justificado.

## 5. Qué se aprende

- La regresión no busca pasar por los puntos: busca la tendencia.
- Más coeficientes siempre reducen $S_r$; el criterio es el error estándar
  ajustado por grados de libertad (17.20).
- Un modelo de calibración debe ser **estable y defendible**, no el de mayor
  $r^2$.

## 6. Límites

- Los datos son sintéticos y didácticos; no sustituyen una calibración real.
- No se modela histéresis ni deriva térmica.
- La validación cruzada es de un solo punto; en producción se usa $k$-fold.
