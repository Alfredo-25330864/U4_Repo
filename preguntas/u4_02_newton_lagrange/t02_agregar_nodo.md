---
id: t02_agregar_nodo
titulo: Agregar un nodo a la forma de Newton
---

El polinomio de Newton se escribe

$$f_n(x)=b_0+b_1(x-x_0)+\cdots+b_n(x-x_0)\cdots(x-x_{n-1}) \tag{18.7}$$

y los coeficientes $b_k$ son la diagonal de la tabla de diferencias divididas.

**Si ya tienes el polinomio de grado $n$ y consigues un dato nuevo en
$x_{n+1}$, ¿qué trabajo extra exige la forma de Newton?**

- [x] Sólo calcular la siguiente diagonal y añadir un término; los coeficientes anteriores no cambian
- [ ] Recalcular la tabla completa desde el primer nodo, porque todos los coeficientes cambian
- [ ] Cambiar el orden de los nodos para que $x_{n+1}$ quede primero
- [ ] Nada: la forma de Newton es de grado fijo y no admite más nodos
