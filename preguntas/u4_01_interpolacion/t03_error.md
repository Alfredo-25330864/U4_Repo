---
id: t03_error
titulo: De qué depende el error de truncamiento
---

Para un polinomio de interpolación de grado $n$, el error es

$$R_n=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-x_0)(x-x_1)\cdots(x-x_n).$$

**De acuerdo con esa expresión, ¿qué controla la magnitud del error?**

- [ ] Sólo el grado del polinomio: más grado siempre es menos error
- [ ] Sólo la derivada de la función en el intervalo
- [x] El producto de las distancias del punto a cada nodo, además del grado y de la derivada
- [ ] Sólo la separación entre el primer y el último nodo
