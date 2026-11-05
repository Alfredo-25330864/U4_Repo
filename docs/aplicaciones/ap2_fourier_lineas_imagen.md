# AP2 — Imagen de líneas con series de Fourier

| ⬅️ Índice de aplicaciones | 🏠 Inicio |
|:---|:---:|
| [Aplicaciones](aplicaciones_index.md) | [README](../../README.md) |

> **Tipo:** aplicación propuesta (extensión). El ajuste sinusoidal es contenido
> del libro (sección 19.1); el procesamiento de una imagen de líneas es nuestro.

## 1. Problema

Una cámara industrial mira una pieza con franjas claras y oscuras. Queremos

1. representar el **perfil de intensidad** de una fila de la imagen con pocos
   armónicos de Fourier,
2. reconstruir el perfil y localizar los **bordes** (transiciones claro/oscuro),
3. medir cuánto se pierde al quedarse con $m$ armónicos.

## 2. Del libro a la imagen

**📘 Del libro.** Una función periódica se aproxima con

$$f(t)=A_0+\sum_{j=1}^{m}\left[A_j\cos(j\omega_0t)+B_j\sin(j\omega_0t)\right],$$

y para datos igualmente espaciados los coeficientes son

$$A_0=\frac{\sum y}{N},\qquad
A_j=\frac{2}{N}\sum y\cos(j\omega_0t),\qquad
B_j=\frac{2}{N}\sum y\sin(j\omega_0t), \tag{19.14–19.16}$$

que es la generalización del ajuste de una sola sinusoide (19.11). El libro
presenta además la serie de Fourier continua (19.2), la DFT (19.5) y la FFT
(19.6).

**🧮 Puente con la imagen.** Una fila de la imagen es una señal 1-D: la
intensidad $y(x)$ muestreada en $N$ píxeles. Si las franjas son periódicas,
esa señal se representa con pocos armónicos. El **periodo** se estima con la
separación entre franjas; la **frecuencia fundamental** es
$\omega_0=2\pi/T$.

## 3. Procedimiento

1. **Generar o cargar la imagen.** Para que el cuaderno sea reproducible, se
   genera una imagen sintética de $128\times128$ píxeles con franjas
   verticales, un gradiente suave y ruido.
2. **Extraer el perfil.** Tomar la fila central: `perfil = imagen[N//2, :]`.
3. **Estimar el periodo.** Contar cruces por cero o usar la FFT
   (`np.fft.rfft`) para encontrar el pico dominante.
4. **Ajustar la serie.** Calcular $A_0$, $A_j$, $B_j$ con
   `coeficientes_fourier`.
5. **Reconstruir** con $m=1,3,5,10$ armónicos y comparar contra el perfil
   original.
6. **Detectar bordes.** Los bordes son máximos de $|f'(x)|$; se comparan con
   los bordes de la imagen ideal.

## 4. Verificación

| Comprobación | Criterio |
|---|---|
| Reconstrucción con todos los armónicos | error cuadrático medio $\approx0$ |
| Reconstrucción con $m$ pequeño | el ECM baja al subir $m$ |
| Bordes detectados | coinciden con la posición conocida de las franjas |
| Perfil ruidoso | la serie suaviza el ruido sin mover los bordes |

## 5. Qué se aprende

- Fourier es **regresión con una base de senos y cosenos**, no interpolación.
- La elección de $m$ es la misma disyuntiva que el grado del polinomio:
  poco $m$ suaviza, mucho $m$ copia el ruido.
- La FFT del libro (sección 19.6) es la versión eficiente de estas sumas; en
  NumPy se usa `np.fft.rfft`. Se menciona como extensión, no se implementa
  desde cero.

## 6. Límites de la aplicación

- Se trabaja en **una dimensión** (una fila o columna), no en 2-D.
- Se supone que las franjas son verticales y el periodo constante.
- Si la imagen tiene perspectiva o iluminación no uniforme, el modelo
  sinusoidal simple no basta; habría que corregir primero.
