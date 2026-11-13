---
id: t01_diferencias
titulo: Qué mide una diferencia dividida
---

La tabla de diferencias divididas se construye con

$$f[x_i,x_j]=\frac{f(x_i)-f(x_j)}{x_i-x_j}
\qquad\text{y}\qquad
f[x_i,x_j,x_k]=\frac{f[x_i,x_j]-f[x_j,x_k]}{x_i-x_k} \tag{18.13}$$

**¿Qué información aporta la diferencia de segundo orden $f[x_i,x_j,x_k]$?**

- [ ] El valor de la función en el nodo intermedio $x_j$
- [x] La razón de cambio de la pendiente, es decir, una aproximación a la segunda derivada
- [ ] El promedio de las tres pendientes de la tabla
- [ ] El error cometido al interpolar con una recta entre $x_i$ y $x_k$
