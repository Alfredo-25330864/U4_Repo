# 🗺️ Plan — Repositorio U4: Ajuste de Curvas e Interpolación

> Plan de trabajo por fases. Se ejecuta de forma incremental.

## Decisiones base

- **Ubicación:** carpeta nueva `U4_Repo/` dentro de
  `U4 Ajuste de curvas e interpolación/`, en paralelo a `U3_Repo`.
- **Cuadernos:** 4 (interpolación, Newton–Lagrange, mínimos cuadrados,
  aplicaciones).
- **Teoría:** 5 documentos en `docs/metodos/` + 3 fichas en
  `docs/aplicaciones/`.
- **Biblioteca:** `lib/robomat.py` (copiado de U3, sin cambios de API) +
  `lib/ajuste_curvas.py` (funciones nuevas).
- **Pruebas:** `tests/test_ajuste_curvas.py` con `unittest`, sin dependencias
  extra.
- **No tocar:** `U3_Repo/`, `U3_T1/`, `Contenido/Markdown/**`.

## Alcance temático

| Tema del programa | Dónde vive |
|---|---|
| 4.1 Interpolación lineal y cuadrática | `docs/metodos/01_*`, cuaderno 01 |
| 4.2 Newton y Lagrange | `docs/metodos/02_*`, `03_*`, cuaderno 02 |
| 4.3 Mínimos cuadrados lineal y cuadrático | `docs/metodos/04_*`, cuaderno 03 |
| 4.4 Aplicaciones | `docs/aplicaciones/*`, cuaderno 04 |

## Fases

### Fase 0 — Estructura

- [x] Crear `U4_Repo/` con `docs/metodos/`, `docs/aplicaciones/`,
      `notebooks/`, `lib/`, `tests/`, `config/`, `tools/`.
- [x] `.gitignore` y `pyrightconfig.json` (espejo de U3).
- [x] Copiar `lib/robomat.py` sin modificar su API.

### Fase 1 — Documentación

- [x] `docs/metodos/01_interpolacion_lineal_cuadratica.md`
- [x] `docs/metodos/02_newton_diferencias_divididas.md`
- [x] `docs/metodos/03_lagrange.md`
- [x] `docs/metodos/04_minimos_cuadrados_lineal_cuadratico.md`
- [x] `docs/metodos/05_comparativa_interpolacion_regresion.md`
- [x] `docs/aplicaciones/` (índice + 3 fichas)
- [x] `docs/casos_estudio/` (índice + 4 casos con problema, método y comparación)
- [x] `docs/figuras/` y `tools/generar_figuras.py` (figuras reproducibles)

### Fase 2 — Biblioteca y pruebas

- [x] `lib/ajuste_curvas.py` con Newton, Lagrange, mínimos cuadrados,
      Fourier e interpolación parabólica.
- [x] `tests/test_ajuste_curvas.py` contra los ejemplos del libro.
- [x] `lib/mn_motor/` recuperado de la rama `test` de U3 y adaptado a U4
      (ajustes, recursos, comparación de escalares).
- [x] `lib/mn_motor/solvers_u4.py` con referencias exactas de U4.
- [x] `preguntas/` con el contrato y el índice vacío del Cuaderno 01.
- [x] `tests/test_mn_motor.py` (rama `test`).

### Fase 2.5 — Grader (pendiente)

- [ ] Preguntas de los cuatro cuadernos en `preguntas/`.
- [ ] `tools/build_grader.py` adaptado a U4.
- [ ] Blob `grader/u4_*.txt` y celda de calificación en los cuadernos.

### Fase 3 — Cuadernos

- [x] `U4_01_Interpolacion.ipynb`
- [x] `U4_02_Newton_Lagrange.ipynb`
- [x] `U4_03_Minimos_Cuadrados.ipynb`
- [x] `U4_04_Aplicaciones.ipynb`

### Fase 4 — Verificación

- [x] Ejecutar `python -m unittest discover -s tests -v`.
- [x] Ejecutar los cuadernos con `jupyter nbconvert --execute`.
- [x] Revisar que no haya outputs guardados de más.

### Pendiente (si se publica)

- [ ] Repositorio remoto y URL en los cuadernos.
- [ ] Autograder con Apps Script (reutilizar el motor de U3).
- [ ] Preguntas sembradas por Número de Control.

### Fase 5 — Codespaces y publicación (por decidir)

- [x] `.devcontainer/devcontainer.json` + `requirements.txt`.
- [ ] `ejercicios/` con una función por archivo y `if __name__ == "__main__":`.
- [ ] Semilla por NC compartida con `mn_motor`.
- [x] Generador de sitio (Pandoc + MathJax) y workflow de GitHub Pages.
- [ ] GitHub Actions para correr pruebas además de publicar.

## Orden de ejecución

```text
Fase 0 ──► Fase 1 ──► Fase 2 ──► Fase 3 ──► Fase 4
```
