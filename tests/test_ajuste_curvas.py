"""Pruebas de ``lib/ajuste_curvas.py`` contra los ejemplos del libro.

Se ejecutan sin dependencias extra:

    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))

import ajuste_curvas as ac  # noqa: E402


class TestNewton(unittest.TestCase):
    def setUp(self):
        self.x = np.array([1.0, 4.0, 6.0])
        self.f = np.array([0.0, 1.386294, 1.791759])

    def test_lineal_libro(self):
        f1 = ac.newton([1.0, 6.0], [0.0, 1.791759], 2.0)
        self.assertAlmostEqual(f1, 0.3583519, places=6)

    def test_cuadratica_libro(self):
        b = ac.coeficientes_newton(self.x, self.f)
        np.testing.assert_allclose(b, [0.0, 0.4620981, -0.0518731], atol=1e-7)
        self.assertAlmostEqual(ac.evaluar_newton(self.x, b, 2.0), 0.5658444, places=6)

    def test_cubica_libro(self):
        x = np.append(self.x, 5.0)
        y = np.append(self.f, 1.609438)
        b = ac.coeficientes_newton(x, y)
        # Tolerancias holgadas: el libro tabula sólo 6 decimales de f(5).
        self.assertAlmostEqual(b[3], 0.007865529, places=6)
        self.assertAlmostEqual(ac.evaluar_newton(x, b, 2.0), 0.6287686, places=5)


class TestLagrange(unittest.TestCase):
    def test_reproduce_nodos(self):
        x = np.array([0.0, 1.5, 3.0, 4.2])
        y = np.array([1.0, -2.0, 0.5, 3.0])
        np.testing.assert_allclose(ac.evaluar_lagrange(x, y, x), y, atol=1e-12)

    def test_concuerda_con_newton(self):
        x = np.array([1.0, 4.0, 6.0])
        y = np.array([0.0, 1.386294, 1.791759])
        xx = np.linspace(0.5, 7.0, 25)
        np.testing.assert_allclose(ac.evaluar_lagrange(x, y, xx),
                                   ac.newton(x, y, xx), atol=1e-9)

    def test_ejemplo_18_6(self):
        x = np.array([1.0, 4.0, 6.0])
        y = np.array([0.0, 1.386294, 1.791760])
        self.assertAlmostEqual(ac.evaluar_lagrange(x, y, 2.0), 0.5658444, places=6)


class TestMinimosCuadrados(unittest.TestCase):
    def test_lineal_tabla_17_1(self):
        x = np.arange(1.0, 8.0)
        y = np.array([0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5])
        r = ac.minimos_cuadrados(x, y, 1)
        np.testing.assert_allclose(r["coef"], [0.07142857, 0.8392857], atol=1e-7)
        self.assertAlmostEqual(r["Sr"], 2.9911, places=3)
        self.assertAlmostEqual(r["syx"], 0.7735, places=3)
        self.assertAlmostEqual(r["r2"], 0.868, places=3)

    def test_cuadratica_tabla_17_4(self):
        x = np.arange(0.0, 6.0)
        y = np.array([2.1, 7.7, 13.6, 27.2, 40.9, 61.1])
        r = ac.minimos_cuadrados(x, y, 2)
        np.testing.assert_allclose(r["coef"], [2.47857, 2.35929, 1.86071], atol=1e-4)
        self.assertAlmostEqual(r["Sr"], 3.74657, places=3)
        self.assertAlmostEqual(r["r2"], 0.99851, places=4)
        self.assertAlmostEqual(r["syx"], 1.12, places=2)

    def test_polinomio_exacto(self):
        # Con datos de un polinomio de grado m el ajuste lo recupera.
        x = np.linspace(-2, 3, 12)
        y = 1.5 - 2 * x + 0.75 * x ** 2
        r = ac.minimos_cuadrados(x, y, 2)
        np.testing.assert_allclose(r["coef"], [1.5, -2.0, 0.75], atol=1e-10)

    def test_grado_de_interpolacion_no_estima_syx(self):
        # n = m + 1: el modelo interpola, no quedan grados de libertad.
        x = np.arange(6.0)
        y = np.array([2.1, 7.7, 13.6, 27.2, 40.9, 61.1])
        r = ac.minimos_cuadrados(x, y, 5)
        self.assertEqual(r["grados_libertad"], 0)
        self.assertTrue(np.isinf(r["syx"]))
        self.assertLess(r["Sr"], 1e-15)


class TestFourier(unittest.TestCase):
    def test_ejemplo_19_1(self):
        t = np.arange(0, 1.36, 0.15)
        y = np.array([2.200, 1.595, 1.031, 0.722, 0.786,
                      1.200, 1.805, 2.369, 2.678, 2.614])
        r = ac.ajuste_sinusoidal(t, y, 4.189)
        self.assertAlmostEqual(r["A0"], 1.7, places=3)
        self.assertAlmostEqual(r["A1"], 0.500, places=3)
        self.assertAlmostEqual(r["B1"], -0.866, places=3)
        self.assertAlmostEqual(r["C1"], 1.00, places=3)
        self.assertAlmostEqual(r["theta"], 1.0472, places=3)

    def test_coeficientes_reconstruyen_senal(self):
        t = np.linspace(0, 1, 64, endpoint=False)
        y = 2.0 + 1.5 * np.cos(2 * np.pi * t) + 0.5 * np.sin(4 * np.pi * t)
        coef = ac.coeficientes_fourier(t, y, 2 * np.pi, 2)
        self.assertAlmostEqual(coef["A0"], 2.0, places=10)
        np.testing.assert_allclose(coef["A"], [1.5, 0.0], atol=1e-10)
        np.testing.assert_allclose(coef["B"], [0.0, 0.5], atol=1e-10)
        np.testing.assert_allclose(ac.evaluar_fourier(t, coef, 2 * np.pi), y, atol=1e-10)


class TestParabolica(unittest.TestCase):
    def f(self, x):
        return 2 * np.sin(x) - x ** 2 / 10

    def test_ecuacion_13_7(self):
        x3 = ac.x_parabolico(0.0, 1.0, 4.0, 0.0, 1.5829, -3.1136)
        self.assertAlmostEqual(x3, 1.5055, places=4)

    def test_converge_al_maximo(self):
        r = ac.interpolacion_parabolica(self.f, 0.0, 1.0, 4.0, tol=1e-8)
        self.assertAlmostEqual(r["x_opt"], 1.4276, places=3)
        self.assertAlmostEqual(r["f_opt"], 1.7757, places=3)


if __name__ == "__main__":
    unittest.main()
