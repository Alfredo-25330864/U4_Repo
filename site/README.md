# Sitio de teoría (GitHub Pages)

Este sitio convierte los `.md` de `docs/` a HTML con **Pandoc** y renderiza las
matemáticas con **MathJax 3** configurado con `tags: 'ams'`. Así:

- `\tag{18.2}` sí numera la ecuación;
- las matrices usan `\\` normal para cambiar de fila;
- no dependes del renderizador de GitHub, que falla con matrices dentro de
  tablas y con `\\`.

## Construir en local

```bash
pandoc --version          # necesita Pandoc 3+
python tools/build_site.py
```

El resultado queda en `_site/`. Ábrelo con cualquier servidor estático:

```bash
python -m http.server -d _site 8000
```

## Publicar

1. Sube el repositorio a GitHub.
2. En **Settings → Pages**, elige **GitHub Actions** como fuente.
3. Haz push a `main`. El workflow `.github/workflows/pages.yml` construye y
   publica.

## Reglas de escritura

- Las matrices van en **bloque propio**, no dentro de una tabla Markdown.
- Usa `$$...$$` para ecuaciones desplegadas y `$...$` para inline.
- Las figuras se referencian con rutas relativas (`../figuras/...`).
- Si una ecuación lleva número, usa `\tag{...}`; MathJax lo respeta.
