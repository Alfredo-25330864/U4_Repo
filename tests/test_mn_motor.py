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
import sympy as sp  # noqa: E402


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
        b = solvers.coeficientes_newton(x, y)
        self.assertAlmostEqual(float(b[1]), 0.4620981, places=6)
        self.assertAlmostEqual(float(b[2]), -0.0518731, places=6)
        self.assertAlmostEqual(float(solvers.interpolacion_newton(x, y, 2)),
                               0.5658442, places=6)

    def test_tabla_diferencias_es_triangular(self):
        x = [1, 4, 6, 5]
        y = [0, 1.386294, 1.791759, 1.609438]
        T = solvers.tabla_diferencias(x, y)
        self.assertEqual(len(T), 4)
        self.assertEqual(len(T[0]), 4)
        self.assertAlmostEqual(float(T[3][3]), 0.007865529, places=6)
        self.assertEqual([T[i][i] for i in range(4)],
                         solvers.coeficientes_newton(x, y))

    def test_lagrange_concuerda_con_newton(self):
        x = [1, 4, 6, 5]
        y = [0, 1.386294, 1.791759, 1.609438]
        for xx in (1.5, 2, 4.5, 5.5):
            self.assertAlmostEqual(
                float(solvers.interpolacion_lagrange(x, y, xx)),
                float(solvers.interpolacion_newton(x, y, xx)), places=9)

    def test_regresion_lineal_exacta(self):
        x = [1, 2, 3, 4, 5, 6, 7]
        y = [0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5]
        a0, a1 = solvers.regresion_lineal(x, y)
        self.assertEqual(a0, sp.Rational(1, 14))
        self.assertEqual(a1, sp.Rational(47, 56))

    def test_regresion_cuadratica_libro(self):
        x = list(range(6))
        y = [2.1, 7.7, 13.6, 27.2, 40.9, 61.1]
        a = [float(v) for v in solvers.regresion_cuadratica(x, y)]
        for calculado, libro in zip(a, [2.47857, 2.35929, 1.86071]):
            self.assertAlmostEqual(calculado, libro, places=5)

    def test_error_estandar_y_r2(self):
        x = list(range(6))
        y = [2.1, 7.7, 13.6, 27.2, 40.9, 61.1]
        coef = [float(v) for v in solvers.regresion_cuadratica(x, y)]
        sr = float(solvers.suma_residuos_cuadrados(x, y, coef))
        st = float(solvers.suma_cuadrados_total(y))
        self.assertAlmostEqual(sr, 3.74657, places=4)
        self.assertAlmostEqual(float(solvers.error_estandar(sr, 6, 2)), 1.12,
                               places=2)
        self.assertAlmostEqual(float(solvers.coeficiente_determinacion(sr, st)),
                               0.99851, places=4)

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
    CUADERNOS = (
        ('u4_01_interpolacion', 'U4_01_Interpolacion'),
        ('u4_02_newton_lagrange', 'U4_02_Newton_Lagrange'),
        ('u4_03_minimos_cuadrados', 'U4_03_Minimos_Cuadrados'),
        ('u4_04_casos', 'U4_04_Casos'),
    )

    def _marco_ref(self):
        """Un alumno perfecto: las funciones de referencia del solver."""
        import mn_motor.ejercicios_u4 as cat
        return {cat.NOMBRE_FUNCION[m]: getattr(solvers, cat.NOMBRE_FUNCION[m])
                for m in cat.METODOS}

    def test_alumno_perfecto_en_los_cuatro_cuadernos(self):
        marco = self._marco_ref()
        for cuad, tid in self.CUADERNOS:
            mn_motor.usar_cuaderno(cuad, tid)
            t = mn_motor.generar_tarea("m16330887@hermosillo.tecnm.mx", "Prueba")
            self.assertTrue(t['preguntas'], cuad)
            for i in range(len(t['preguntas'])):
                t['respuestas'][i] = None
            puntos = sum(califica.acierto(q, None, marco) for q in t['preguntas'])
            self.assertEqual(puntos, len(t['preguntas']), cuad)

    def test_alumno_sin_funciones_no_puntua(self):
        mn_motor.usar_cuaderno(*self.CUADERNOS[0])
        t = mn_motor.generar_tarea("m16330887@hermosillo.tecnm.mx", "Prueba")
        self.assertEqual(sum(califica.acierto(q, None, {}) for q in t['preguntas']), 0)

    def test_casos_ocultos_distintos_a_la_actividad_a_mano(self):
        import mn_motor.ejercicios_u4 as cat
        import mn_motor.mano as mano
        alumno = "m16330887@hermosillo.tecnm.mx"
        mn_motor.usar_cuaderno(*self.CUADERNOS[0])
        t = mn_motor.generar_tarea(alumno, "Prueba")
        q = t['preguntas'][0]
        entrada_mano = cat.elegir_mano(
            'INTERP_LINEAL', comun.rng_de(alumno, mano._sal('INTERP_LINEAL')))['datos']
        primera_mano = (entrada_mano['x0'], entrada_mano['f0'],
                        entrada_mano['x1'], entrada_mano['f1'], entrada_mano['x'])
        self.assertNotIn(primera_mano, [c[0] for c in q['casos']])


class TestMano(unittest.TestCase):
    ALUMNO = "m16330887@hermosillo.tecnm.mx"

    def test_ejercicio_determinista(self):
        import mn_motor.ejercicios_u4 as cat
        import mn_motor.mano as mano
        rng1 = comun.rng_de(self.ALUMNO, mano._sal('REG_LINEAL'))
        rng2 = comun.rng_de(self.ALUMNO, mano._sal('REG_LINEAL'))
        a = cat.elegir_mano('REG_LINEAL', rng1)
        b = cat.elegir_mano('REG_LINEAL', rng2)
        self.assertEqual(a['datos'], b['datos'])

    def test_alumnos_distintos_reciben_datos_distintos(self):
        import mn_motor.ejercicios_u4 as cat
        import mn_motor.mano as mano
        a = cat.elegir_mano('NEWTON_TABLA',
                            comun.rng_de(self.ALUMNO, mano._sal('NEWTON_TABLA')))
        b = cat.elegir_mano('NEWTON_TABLA',
                            comun.rng_de("m99999999@hermosillo.tecnm.mx",
                                         mano._sal('NEWTON_TABLA')))
        self.assertNotEqual(a['datos'], b['datos'])

    def test_tolera_truncado_y_redondeo(self):
        ref = 0.5658444
        self.assertTrue(comun.cerca_relativa(0.5658, ref, 1.5e-4))   # truncado
        self.assertTrue(comun.cerca_relativa(0.5658, ref, 1.5e-4))   # redondeo
        self.assertFalse(comun.cerca_relativa(0.565, ref, 1.5e-4))   # 3 decimales

    def test_comprueba_comparaciones(self):
        import math
        self.assertFalse(comun.cerca_relativa("x", 1.0, 1e-4))
        self.assertFalse(comun.cerca_relativa(math.nan, 1.0, 1e-4))
        self.assertTrue(comun.cerca_relativa(0, 0, 1e-4))


if __name__ == "__main__":
    unittest.main()

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
