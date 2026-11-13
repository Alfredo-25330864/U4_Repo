---
id: t04_error_estandar
titulo: El error estándar de la estimación
---

El error estándar de la estimación se define como

$$s_{y/x}=\sqrt{\frac{S_r}{n-(m+1)}}$$

donde $m$ es el grado del polinomio ajustado.

**¿Por qué se divide entre $n-(m+1)$ y no entre $n$?**

- [ ] Porque así el resultado siempre es menor que el error real
- [x] Porque se perdieron $m+1$ grados de libertad al estimar los coeficientes con los mismos datos
- [ ] Porque $n$ incluye el punto que se quiere predecir
- [ ] Porque $S_r$ ya está dividido entre $n$ dentro de la suma
