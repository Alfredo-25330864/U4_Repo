---
id: t03_lagrange
titulo: Por qué Lagrange no usa diferencias divididas
---

Los polinomios de Lagrange son

$$L_i(x)=\prod_{\substack{j=0\\ j\neq i}}^{n}\frac{x-x_j}{x_i-x_j}
\qquad\text{y}\qquad
f_n(x)=\sum_{i=0}^{n}L_i(x)\,f(x_i) \tag{18.20}$$

**Cada $L_i$ vale $1$ en $x_i$ y $0$ en los demás nodos. ¿Para qué sirve esa
propiedad?**

- [ ] Para ordenar los nodos de menor a mayor antes de evaluar
- [x] Para que al sumar $L_i(x)f(x_i)$ el polinomio pase exactamente por cada punto conocido
- [ ] Para que el polinomio tenga grado $n+1$ en lugar de $n$
- [ ] Para evitar dividir entre las diferencias de los nodos
