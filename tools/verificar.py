"""Ejecuta las pruebas de la unidad desde cualquier carpeta.

    python tools/verificar.py
"""

import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    raise SystemExit(subprocess.call(
        [sys.executable, "-m", "unittest", "discover", "-s",
         os.path.join(RAIZ, "tests"), "-v"],
        cwd=RAIZ,
    ))
