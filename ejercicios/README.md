# Ejercicios de la Unidad 4

Un archivo por **algoritmo**. Cada uno trae la función esqueleto y un bloque
`if __name__ == "__main__":` con un ejemplo genérico para probarla antes de
llevarla al cuaderno.

```bash
# desde la raíz del repositorio
python -m ejercicios.interpolacion.interpolacion_lineal
python -m ejercicios.newton_lagrange.interpolacion_newton
```

El ejemplo del bloque `__main__` **no** es el tuyo: el ejercicio de tu número
de control sale en el cuaderno. Aquí sólo compruebas la firma y la lógica.

## Reglas

1. No cambies el nombre ni los parámetros de la función.
2. El método completo debe **llamar** a sus funciones auxiliares, no repetir la
   cuenta: así se prueba cada pieza por separado.
3. Devuelve `float` o `list[float]`. Nada de imprimir dentro de la función.
4. Si un archivo importa a otro, ejecútalo como módulo (`python -m ...`), no
   como script suelto.

## Mapa

| Carpeta | Cuaderno | Algoritmos |
|---|---|---|
| `interpolacion/` | 01 | lineal, coeficientes, cuadrática, error |
| `newton_lagrange/` | 02 | tabla, coeficientes, evaluación, Lagrange, error |
| `minimos_cuadrados/` | 03 | Sr, lineal, cuadrática, sy/x, r² |
| `casos/` | 04 | Fourier (tarea extra) |
