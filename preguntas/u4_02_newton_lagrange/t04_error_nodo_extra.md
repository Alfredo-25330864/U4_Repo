---
id: t04_error_nodo_extra
titulo: Estimar el error sin conocer la función
---

Cuando se tiene un nodo más de los necesarios, el error se estima con

$$R_n\cong f[x_{n+1},x_n,\dots,x_0]\prod_{i=0}^{n}(x-x_i) \tag{18.18}$$

**En el cuaderno esto se calcula comparando la predicción de grado $n+1$ con
la de grado $n$. ¿Por qué esa diferencia sirve como estimación del error?**

- [ ] Porque el polinomio de grado $n+1$ es exacto y el de grado $n$ no
- [x] Porque el término que aporta el nodo extra es, hasta el factor $\prod(x-x_i)$, justo la diferencia de orden $n+1$ de la fórmula del error
- [ ] Porque promediar dos polinomios reduce el error a la mitad
- [ ] Porque el error real siempre es menor que esa diferencia
