"""Pruebas del motor de calificación y de sus solvers de referencia.

    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))

import mn_motor  # noqa: E402
import mn_motor.califica as califica  # noqa: E402
import mn_motor.comun as comun  # noqa: E402
import mn_motor.solvers_u4 as solvers  # noqa: E402


class TestComun(unittest.TestCase):
    def test_extraer_nc(self):
        self.assertEqual(comun.extraer_nc("m16330887@hermosillo.tecnm.mx"), "16330887")
        self.assertEqual(comun.extraer_nc("16330887@tecnm.mx"), "16330887")
        self.assertEqual(comun.extraer_nc("m{12345678}@tecnm.mx"), "12345678")

    def test_semilla_estable_y_distinta(self):
        a = comun.semilla_de("m16330887@hermosillo.tecnm.mx")
        b = comun.semilla_de("m16330887@hermosillo.tecnm.mx")
        c = comun.semilla_de("m99999999@hermosillo.tecnm.mx")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_comparar_varias_matrices(self):
        esperado = [[[1, 2], [3, 4]], [[5], [6]]]
        respuesta = [[[1.0, 2.0], [3.0, 4.0]], [[5.0], [6.0]]]
        self.assertTrue(comun.comparar(respuesta, esperado))
        self.assertFalse(comun.comparar([[[1, 2]], [[5]]], esperado))

    def test_numero_igual(self):
        self.assertTrue(comun.numero_igual(0.5658442, 0.5658444))
        self.assertFalse(comun.numero_igual(0.56, 0.57))


class TestSolversU4(unittest.TestCase):
    def test_newton_cuadratica_libro(self):
        x = [1, 4, 6]
        y = [0, 1.386294, 1.791759]
        b = solvers.diferencias_divididas(x, y)
        self.assertAlmostEqual(float(b[1]), 0.4620981, places=6)
        self.assertAlmostEqual(float(b[2]), -0.0518731, places=6)
        self.assertAlmostEqual(float(solvers.newton(x, y, 2)), 0.5658442, places=6)

    def test_lagrange_concuerda_con_newton(self):
        x = [1, 4, 6, 5]
        y = [0, 1.386294, 1.791759, 1.609438]
        for xx in (1.5, 2, 4.5, 5.5):
            self.assertAlmostEqual(float(solvers.evaluar_lagrange(x, y, xx)),
                                   float(solvers.newton(x, y, xx)), places=9)

    def test_minimos_cuadrados_lineal_exacto(self):
        x = [1, 2, 3, 4, 5, 6, 7]
        y = [0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5]
        a0, a1 = solvers.minimos_cuadrados(x, y, 1)
        self.assertEqual(a0, __import__("sympy").Rational(1, 14))
        self.assertEqual(a1, __import__("sympy").Rational(47, 56))

    def test_minimos_cuadrados_cuadratico_libro(self):
        x = list(range(6))
        y = [2.1, 7.7, 13.6, 27.2, 40.9, 61.1]
        a = [float(v) for v in solvers.minimos_cuadrados(x, y, 2)]
        for calculado, libro in zip(a, [2.47857, 2.35929, 1.86071]):
            self.assertAlmostEqual(calculado, libro, places=5)

    def test_fourier_ejemplo_19_1(self):
        t = [0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.35]
        y = [2.200, 1.595, 1.031, 0.722, 0.786,
             1.200, 1.805, 2.369, 2.678, 2.614]
        A0, A, B = solvers.coeficientes_fourier(t, y, 4.189, 1)
        self.assertAlmostEqual(float(A0), 1.7, places=6)
        self.assertAlmostEqual(float(A[0]), 0.500, places=3)
        self.assertAlmostEqual(float(B[0]), -0.866, places=3)

    def test_parabolica_13_7(self):
        x3 = solvers.x_parabolico(0, 1, 4, 0, 1.5829, -3.1136)
        self.assertAlmostEqual(float(x3), 1.5055, places=4)


class TestMotor(unittest.TestCase):
    def test_api_publica(self):
        for nombre in ("generar_tarea", "calificar", "practica", "pregunta",
                       "enviar", "usar_cuaderno", "cuaderno"):
            self.assertTrue(hasattr(mn_motor, nombre), nombre)

    def test_usar_cuaderno(self):
        mn_motor.usar_cuaderno("u4_01_interpolacion", "U4_01_Interpolacion")
        self.assertEqual(mn_motor.cuaderno(), "u4_01_interpolacion")

    def test_generar_tarea_vacia(self):
        mn_motor.usar_cuaderno("u4_01_interpolacion", "U4_01_Interpolacion")
        t = mn_motor.generar_tarea("m16330887@hermosillo.tecnm.mx", "Prueba")
        self.assertEqual(t["cuaderno"], "u4_01_interpolacion")
        self.assertEqual(t["nc"], "16330887")
        self.assertEqual(t["preguntas"], [])

    def test_acierto_mcq_numero_matriz(self):
        q_mcq = {"tipo": "mcq", "esperado": 2}
        q_num = {"tipo": "numero", "esperado": 0.5658444}
        q_mat = {"tipo": "matriz", "esperado": [[1, 2], [3, 4]]}
        self.assertEqual(califica.acierto(q_mcq, "2"), 1)
        self.assertEqual(califica.acierto(q_mcq, "1"), 0)
        self.assertEqual(califica.acierto(q_num, "0.5658442"), 1)
        self.assertEqual(califica.acierto(q_num, "0.57"), 0)
        self.assertEqual(califica.acierto(q_mat, "[[1,2],[3,4]]"), 1)
        self.assertEqual(califica.acierto(q_mat, "[[1,2],[3,5]]"), 0)

    def test_acierto_funcion(self):
        q = {"tipo": "funcion", "funcion": "doble", "casos": [((2,), 4), ((3,), 6)]}

        def doble(x):
            return 2 * x

        self.assertEqual(califica.acierto(q, None, {"doble": doble}), 1)
        self.assertEqual(califica.acierto(q, None, {}), 0)


if __name__ == "__main__":
    unittest.main()
