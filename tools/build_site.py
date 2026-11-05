"""Construye el sitio de teoría para GitHub Pages con Pandoc + MathJax.

Uso:
    python tools/build_site.py
    python tools/build_site.py --salida _site

Por qué Pandoc y no el renderizador de GitHub:
  - MathJax se configura aquí (`tags: 'ams'`), así que `\\tag{18.2}` funciona.
  - Las matrices se escriben normal, con `\\\\` para cambiar de fila.
  - El Markdown se convierte a HTML antes de publicar; GitHub Pages sólo sirve
    archivos estáticos.
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, "docs")
SITIO = os.path.join(RAIZ, "site")


def titulo_de(ruta):
    """Primer encabezado H1 del archivo, sin Markdown."""
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            if linea.startswith("# "):
                t = linea[2:].strip()
                t = re.sub(r"\$([^$]+)\$", r"\1", t)
                t = re.sub(r"[*_`]", "", t)
                return t
    return os.path.splitext(os.path.basename(ruta))[0]


def _profundidad(relativa):
    return len(relativa.parts) - 1


def _rewrite_links(texto, profundidad):
    """Convierte enlaces .md a .html y arregla el enlace a la portada."""
    inicio = "../" * profundidad

    def cambiar(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        if href.endswith("README.md"):
            # Los docs enlazan ../../README.md a la portada; los README
            # hermanos (casos_estudio/README.md) se quedan en su carpeta.
            if href.startswith("../"):
                return f'href="{inicio}index.html"'
            return 'href="README.html"'
        if ".md" in href:
            return 'href="' + href.replace(".md", ".html") + '"'
        return m.group(0)

    return re.sub(r'href="([^"]+)"', cambiar, texto)


def construir(salida):
    if not shutil.which("pandoc"):
        raise SystemExit("Falta pandoc. Instálalo desde pandoc.org/installing.html")
    if os.path.isdir(salida):
        shutil.rmtree(salida, ignore_errors=True)
    os.makedirs(salida, exist_ok=True)

    # Recursos estáticos
    shutil.copytree(os.path.join(DOCS, "figuras"),
                    os.path.join(salida, "figuras"), dirs_exist_ok=True)
    shutil.copy2(os.path.join(SITIO, "style.css"),
                 os.path.join(salida, "style.css"))

    paginas = []
    for ruta in sorted(Path(DOCS).rglob("*.md")):
        if "figuras" in ruta.parts:
            continue
        relativa = ruta.relative_to(DOCS)
        destino = os.path.join(salida, str(relativa.with_suffix(".html")))
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        profundidad = _profundidad(relativa)
        inicio = "../" * profundidad
        titulo = titulo_de(ruta)

        cmd = [
            "pandoc", str(ruta),
            "--from=markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+smart",
            "--to=html5",
            "--standalone",
            "--mathjax",
            "--template=site/template.html",
            "--toc", "--toc-depth=3",
            "--highlight-style=tango",
            f"--metadata=title={titulo}",
            f"--variable=css_href={inicio}style.css",
            f"--variable=home_href={inicio}index.html",
            "--output", destino,
        ]
        resultado = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True)
        if resultado.returncode != 0:
            raise SystemExit(f"pandoc falló con {ruta}:\n{resultado.stderr}")
        with open(destino, encoding="utf-8") as f:
            texto = f.read()
        with open(destino, "w", encoding="utf-8") as f:
            f.write(_rewrite_links(texto, profundidad))
        paginas.append((str(relativa.with_suffix(".html")), titulo))
        print("html:", os.path.relpath(destino, salida))

    # Portada
    grupos = {
        "Teoría": [p for p in paginas if p[0].startswith("metodos/")],
        "Casos de estudio": [p for p in paginas if p[0].startswith("casos_estudio/")],
        "Aplicaciones": [p for p in paginas if p[0].startswith("aplicaciones/")],
    }
    bloques = []
    for grupo, items in grupos.items():
        if not items:
            continue
        enlaces = "\n".join(
            f'<li><a href="{html.escape(href)}">{html.escape(titulo)}</a></li>'
            for href, titulo in items)
        bloques.append(f"<h2>{grupo}</h2>\n<ul>\n{enlaces}\n</ul>")

    portada = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Métodos Numéricos · Unidad 4</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar"><a href="index.html">Métodos Numéricos · Unidad 4</a></header>
<main>
<h1>Ajuste de curvas e interpolación</h1>
<p>Teoría, casos de estudio y aplicaciones de la Unidad 4. Las ecuaciones se
renderizan con MathJax al construir el sitio, no con el visor de GitHub.</p>
{''.join(bloques)}
</main>
<footer><p>Material del curso · ITH 2026.</p></footer>
</body>
</html>
"""
    with open(os.path.join(salida, "index.html"), "w", encoding="utf-8") as f:
        f.write(portada)
    print("html:", os.path.join(os.path.basename(salida), "index.html"))
    print(f"Listo: {len(paginas)} páginas + portada en {salida}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--salida", default=os.path.join(RAIZ, "_site"),
                    help="carpeta de salida (por omisión: _site/)")
    args = ap.parse_args()
    construir(os.path.abspath(args.salida))


if __name__ == "__main__":
    main()
