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
import mn_motor.solvers_u3 as solvers_u3  # noqa: E402
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
    def test_lineal_devuelve_valor_y_sin_error(self):
        y, error = solvers.interpolacion_lineal(1, 0, 6, 1.791759, 2)
        self.assertAlmostEqual(y, 0.3583519, places=6)
        self.assertIsNone(error)

    def test_lineal_estima_el_error_con_tercer_dato(self):
        y, error = solvers.interpolacion_lineal(1, 0, 4, 1.386294, 2,
                                                x2=6, y2=1.791759)
        self.assertAlmostEqual(y, 0.4620981, places=6)
        # R1 = f[x2,x1,x0]*(x-x0)(x-x1) = -0.0518731 * (1)(-2)
        self.assertAlmostEqual(error, 0.1037462, places=6)

    def test_lineal_sin_error_extra_si_el_error_real_es_cero(self):
        # Datos de una recta: el error estimado debe salir 0.
        y, error = solvers.interpolacion_lineal(1, 3, 3, 7, 2, x2=5, y2=11)
        self.assertAlmostEqual(y, 5.0, places=9)
        self.assertAlmostEqual(error, 0.0, places=9)

    def test_cuadratica_devuelve_valor_y_sin_error(self):
        y, error = solvers.interpolacion_cuadratica(0, 1, 1, 3, 2, 7, 1.5)
        self.assertAlmostEqual(y, 4.75, places=9)
        self.assertIsNone(error)

    def test_cuadratica_estima_el_error_con_cuarto_dato(self):
        # parábola x^2 + x + 1 con un cuarto nodo tomado de la misma parábola:
        # el error debe salir 0.
        y, error = solvers.interpolacion_cuadratica(
            0, 1, 1, 3, 2, 7, 1.5, x3=3, y3=13)
        self.assertAlmostEqual(y, 4.75, places=9)
        self.assertAlmostEqual(error, 0.0, places=9)

    def test_coeficientes_cuadraticos_dos_pendientes(self):
        b0, b1, b2 = solvers.coeficientes_cuadraticos(0, 1, 1, 3, 2, 7)
        self.assertEqual([float(b0), float(b1), float(b2)], [1.0, 2.0, 1.0])

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


class TestSolversU3(unittest.TestCase):
    def test_gauss_resuelve_sistema_entero(self):
        A = [[4, 1, -1], [2, 7, 1], [1, -3, 12]]
        b = [3, 19, 31]
        self.assertEqual(solvers_u3.gauss_solve(A, b), [1.0, 2.0, 3.0])

    def test_gauss_triangulariza(self):
        Ab = solvers_u3.gauss_eliminar([[2, 1], [1, 3]], [4, 7])
        self.assertAlmostEqual(float(Ab[1][0]), 0.0, places=12)
        self.assertAlmostEqual(float(Ab[1][1]), 2.5, places=12)

    def test_lu_reconstruye_la_matriz(self):
        A = sp.Matrix([[4, 1, -1], [2, 7, 1], [1, -3, 12]])
        L, U = solvers_u3.lu_doolittle(A)
        self.assertEqual(sp.Matrix(L) * sp.Matrix(U), A)

    def test_calibracion_usa_gauss_y_coincide_con_la_libreria(self):
        x = [0, 10, 20, 30, 40]
        y = [0.1, 1.1, 2.0, 3.1, 3.9]
        por_gauss = solvers.coeficientes_calibracion(x, y, 1)
        por_normales = solvers.regresion_lineal(x, y)
        for a, b in zip(por_gauss, [float(v) for v in por_normales]):
            self.assertAlmostEqual(a, b, places=9)


class TestMotor(unittest.TestCase):
    CUADERNOS = (
        ('u4_01_interpolacion', 'U4_01_Interpolacion'),
        ('u4_02_newton_lagrange', 'U4_02_Newton_Lagrange'),
        ('u4_03_minimos_cuadrados', 'U4_03_Minimos_Cuadrados'),
        ('u4_04_casos', 'U4_04_Casos'),
    )

    def _marco_ref(self):
        """Un alumno perfecto: las funciones de referencia del motor."""
        import mn_motor.ejercicios_u4 as cat
        import mn_motor.solvers_u3 as u3
        marco = {}
        for m in cat.METODOS:
            nombre = cat.NOMBRE_FUNCION[m]
            if hasattr(solvers, nombre):
                marco[nombre] = getattr(solvers, nombre)
            elif hasattr(u3, nombre):
                marco[nombre] = getattr(u3, nombre)
        return marco

    def test_alumno_perfecto_en_los_cuatro_cuadernos(self):
        marco = self._marco_ref()
        for cuad, tid in self.CUADERNOS:
            mn_motor.usar_cuaderno(cuad, tid)
            t = mn_motor.generar_tarea("m16330887@hermosillo.tecnm.mx", "Prueba")
            self.assertTrue(t['preguntas'], cuad)
            for i, q in enumerate(t['preguntas']):
                # Un alumno perfecto: contesta bien la opción múltiple y define
                # las funciones. Cada cuaderno usa el tipo que le corresponde.
                t['respuestas'][i] = q['esperado'] if q['tipo'] == 'mcq' else None
            puntos = sum(califica.acierto(q, t['respuestas'][i], marco)
                         for i, q in enumerate(t['preguntas']))
            self.assertEqual(puntos, len(t['preguntas']), cuad)

    def test_alumno_sin_funciones_no_puntua(self):
        for cuad, tid in self.CUADERNOS:
            mn_motor.usar_cuaderno(cuad, tid)
            t = mn_motor.generar_tarea("m16330887@hermosillo.tecnm.mx", "Prueba")
            for i in range(len(t['preguntas'])):
                t['respuestas'][i] = None
            self.assertEqual(
                sum(califica.acierto(q, None, {}) for q in t['preguntas']), 0, cuad)

    def test_cuaderno_01_pregunta_teoria_no_codigo(self):
        mn_motor.usar_cuaderno(*self.CUADERNOS[0])
        t = mn_motor.generar_tarea("m16330887@hermosillo.tecnm.mx", "Prueba")
        self.assertTrue(all(q['tipo'] == 'mcq' for q in t['preguntas']))
        for q in t['preguntas']:
            self.assertGreaterEqual(len(q['opciones']), 3)
            self.assertIn(q['esperado'], range(len(q['opciones'])))

    def test_practica_por_nombre_de_metodo(self):
        """`practica` funciona aunque el cuaderno no tenga preguntas de código."""
        from preguntas._fabrica import ejemplo_de
        entrada, esperado = ejemplo_de('INTERP_LINEAL')
        self.assertIsInstance(esperado, list)
        self.assertEqual(len(esperado), 2)       # (y, error)
        self.assertIsNone(esperado[1])           # sin tercer dato no hay error


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
