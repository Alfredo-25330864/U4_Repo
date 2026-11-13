---
id: t01_gauss_normales
titulo: Las ecuaciones normales son un sistema lineal
---

Al ajustar una parábola, las ecuaciones normales forman el sistema

$$\begin{bmatrix}
n & \sum x_i & \sum x_i^2\\
\sum x_i & \sum x_i^2 & \sum x_i^3\\
\sum x_i^2 & \sum x_i^3 & \sum x_i^4
\end{bmatrix}
\begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}=
\begin{bmatrix}\sum y_i\\ \sum x_iy_i\\ \sum x_i^2y_i\end{bmatrix}$$

**¿Por qué conviene resolverlo con eliminación gaussiana con pivoteo en lugar
de despejar a mano?**

- [ ] Porque Gauss da la solución exacta y el despeje no
- [x] Porque la matriz puede volverse mal condicionada (sus entradas crecen como potencias de $x$) y el pivoteo evita dividir entre un pivote casi cero
- [ ] Porque el sistema casi nunca tiene solución única
- [ ] Porque Gauss sólo funciona con matrices simétricas
