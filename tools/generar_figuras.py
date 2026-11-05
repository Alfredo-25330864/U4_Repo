"""Genera las figuras de los casos de estudio de la Unidad 4.

Uso:
    python tools/generar_figuras.py

Las figuras se guardan en docs/figuras/ y se insertan en
docs/casos_estudio/*.md. No se dibujan a mano: todo sale de los mismos
datos y funciones que usan los cuadernos.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "lib"))
import ajuste_curvas as ac  # noqa: E402

SALIDA = os.path.join(RAIZ, "docs", "figuras")
os.makedirs(SALIDA, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 160,
    "font.size": 9,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def guardar(fig, nombre):
    ruta = os.path.join(SALIDA, nombre)
    fig.tight_layout()
    fig.savefig(ruta, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("figura:", os.path.relpath(ruta, RAIZ))


# ======================================================================
# Caso 01 — ln 2 por interpolación
# ======================================================================
def figura_interpolacion():
    x = np.array([1.0, 4.0, 6.0, 5.0])
    f = np.array([0.0, 1.386294, 1.791759, 1.609438])
    verdadero = np.log(2.0)

    xs = np.linspace(0.9, 6.3, 400)
    f1_16 = ac.newton([1.0, 6.0], [0.0, 1.791759], xs)
    f1_14 = ac.newton([1.0, 4.0], [0.0, 1.386294], xs)
    f2 = ac.newton(x[:3], f[:3], xs)
    f3 = ac.newton(x, f, xs)

    pred = {
        "lineal [1,6]": ac.newton([1.0, 6.0], [0.0, 1.791759], 2.0),
        "lineal [1,4]": ac.newton([1.0, 4.0], [0.0, 1.386294], 2.0),
        "cuadrática": ac.newton(x[:3], f[:3], 2.0),
        "cúbica": ac.newton(x, f, 2.0),
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ax1.plot(xs, np.log(xs), "k", lw=2, label="ln x")
    ax1.plot(xs, f1_16, ":", label="lineal [1,6]")
    ax1.plot(xs, f1_14, "--", label="lineal [1,4]")
    ax1.plot(xs, f2, "-", label="cuadrática [1,4,6]")
    ax1.plot(xs, f3, "-.", lw=1.2, label="cúbica [1,4,6,5]")
    ax1.plot(x, f, "o", ms=7, color="tab:red", label="nodos")
    ax1.axvline(2.0, color="0.6", ls=":")
    ax1.plot(2.0, verdadero, "*", ms=12, color="k", label="ln 2")
    ax1.set_xlim(0.9, 6.3)
    ax1.set_ylim(-0.2, 2.0)
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.set_title("Interpolaciones de ln x")
    ax1.legend(fontsize=7, loc="upper left")

    nombres = list(pred)
    errores = [abs(v - verdadero) / verdadero * 100 for v in pred.values()]
    barras = ax2.bar(range(len(nombres)), errores, color="tab:blue")
    ax2.bar_label(barras, fmt="%.1f%%", padding=2, fontsize=8)
    ax2.set_xticks(range(len(nombres)))
    ax2.set_xticklabels(nombres, rotation=15, ha="right", fontsize=8)
    ax2.set_ylabel("error relativo (%)")
    ax2.set_title("Error al estimar ln 2")
    ax2.set_ylim(0, max(errores) * 1.25)

    guardar(fig, "caso01_interpolacion_ln2.png")
    print("  errores ln2:", {k: round(v, 4) for k, v in pred.items()})


# ======================================================================
# Caso 02 — trayectoria de un robot
# ======================================================================
def figura_robot():
    t = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    xr = np.array([0.0, 1.2, 2.1, 3.4, 4.8, 6.0])
    yr = np.array([0.0, 0.8, 1.9, 2.0, 1.4, 0.6])

    tt = np.linspace(0, 5, 500)
    px = ac.newton(t, xr, tt)
    py = ac.newton(t, yr, tt)
    v = np.hypot(np.gradient(px, tt), np.gradient(py, tt))

    rng = np.random.default_rng(7)
    xn = xr + 0.12 * rng.standard_normal(t.size)
    yn = yr + 0.12 * rng.standard_normal(t.size)
    fx = ac.minimos_cuadrados(t, xn, 2)
    fy = ac.minimos_cuadrados(t, yn, 2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ax1.plot(xr, yr, "o", ms=8, label="waypoints")
    ax1.plot(px, py, "-", lw=2, label="Newton grado 5")
    ax1.plot(ac.evaluar_polinomio(fx["coef"], tt),
             ac.evaluar_polinomio(fy["coef"], tt),
             "--", label="mínimos cuadrados grado 2")
    ax1.set_aspect("equal")
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    ax1.set_title("Trayectoria: interpolar vs ajustar")
    ax1.legend(fontsize=7)

    ax2.plot(tt, v, label="rapidez interpolada")
    ax2.axhline(2.0, color="tab:red", ls="--", label="límite 2 m/s")
    ax2.set_xlabel("t (s)")
    ax2.set_ylabel("|v| (m/s)")
    ax2.set_title("Rapidez estimada")
    ax2.legend(fontsize=7)

    guardar(fig, "caso02_robot_trayectoria.png")
    print(f"  rapidez máxima: {v.max():.4f} m/s")


# ======================================================================
# Caso 03 — calibración de un sensor
# ======================================================================
def figura_sensor():
    x = np.arange(0, 100, 10, dtype=float)
    y = np.array([0.2, 0.9, 1.8, 2.5, 3.4, 4.2, 5.4, 6.2, 7.5, 8.4])

    recta = ac.minimos_cuadrados(x, y, 1)
    cuad = ac.minimos_cuadrados(x, y, 2)
    xs = np.linspace(-5, 95, 300)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ax1.plot(x, y, "o", ms=7, label="datos")
    ax1.plot(xs, ac.evaluar_polinomio(recta["coef"], xs), "--",
             label=f"lineal  $s_{{y/x}}={recta['syx']:.3f}$")
    ax1.plot(xs, ac.evaluar_polinomio(cuad["coef"], xs), "-",
             label=f"cuadrática  $s_{{y/x}}={cuad['syx']:.3f}$")
    ax1.set_xlabel("cuentas del sensor")
    ax1.set_ylabel("°C")
    ax1.set_title("Dos modelos de calibración")
    ax1.legend(fontsize=7)

    ax2.stem(x, recta["residuales"], basefmt=" ", label="lineal")
    ax2.plot(x, cuad["residuales"], "o-", ms=3, lw=0.8, label="cuadrática")
    ax2.axhline(0, color="k", lw=0.8)
    ax2.set_xlabel("cuentas del sensor")
    ax2.set_ylabel("residuo (°C)")
    ax2.set_title("Residuales: el lineal deja estructura")
    ax2.legend(fontsize=7)

    guardar(fig, "caso03_sensor_regresion.png")
    print(f"  sensor: syx lineal={recta['syx']:.4f}  cuadrática={cuad['syx']:.4f}")


# ======================================================================
# Caso 04 — imagen de líneas con Fourier
# ======================================================================
def figura_fourier():
    N, periodo = 128, 16
    xx, _ = np.meshgrid(np.arange(N), np.arange(N))
    ideal = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * xx / periodo))
    rng = np.random.default_rng(1)
    imagen = np.clip(ideal + 0.15 * xx / N
                     + 0.05 * rng.standard_normal((N, N)), 0, 1)
    perfil = imagen[N // 2, :]
    t = np.arange(N, dtype=float)
    omega0 = 2 * np.pi / periodo

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ax1.imshow(imagen, cmap="gray", vmin=0, vmax=1)
    ax1.set_title("Imagen sintética de líneas")
    ax1.axis("off")

    ax2.plot(t, ideal[N // 2, :], "k--", lw=1.2, label="perfil ideal")
    ax2.plot(t, perfil, color="0.65", lw=1, label="perfil medido")
    for m, estilo in [(1, ":"), (3, "--"), (5, "-."), (10, "-")]:
        coef = ac.coeficientes_fourier(t, perfil, omega0, m)
        recon = ac.evaluar_fourier(t, coef, omega0)
        ecm = np.sqrt(np.mean((recon - perfil) ** 2))
        ax2.plot(t, recon, estilo, lw=1.2, label=f"m={m} (ECM={ecm:.3f})")
    ax2.set_xlabel("pixel")
    ax2.set_ylabel("intensidad")
    ax2.set_title("Reconstrucción con m armónicos")
    ax2.legend(fontsize=7, ncol=2)

    guardar(fig, "caso04_fourier_lineas.png")


if __name__ == "__main__":
    figura_interpolacion()
    figura_robot()
    figura_sensor()
    figura_fourier()
