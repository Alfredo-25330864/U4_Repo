"""interpolacion_cuadratica — cuaderno 01.

Libro: ecuación (18.3) con los coeficientes (18.4) a (18.6), calculados con dos
pendientes:

    m1 = (y1 - y0) / (x1 - x0)
    m2 = (y2 - y1) / (x2 - x1)
    b0 = y0      b1 = m1      b2 = (m2 - m1) / (x2 - x0)

y después se evalúa la forma anidada
``f2(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1)``.

Devuelve **dos** cosas: el valor interpolado y el error.
"""

from ejercicios.interpolacion.error_estimado_interpolacion import (
    error_estimado_interpolacion,
)


def interpolacion_cuadratica(x0, y0, x1, y1, x2, y2, x, x3=None, y3=None):
    """Devuelve ``(y, error)``.

    y     : valor interpolado con la parábola que pasa por los tres nodos.
    error : ``None`` si no hay cuarto dato; si lo hay,
            ``R2 = f[x3,x2,x1,x0] * (x - x0)(x - x1)(x - x2)``.

    x3, y3 son OPCIONALES: puedes terminar el método sin usarlos y, cuando
    escribas ``error_estimado_interpolacion``, regresar aquí y activarlos.
    """
    # m1 = (y1 - y0) / (x1 - x0)
    # m2 = (y2 - y1) / (x2 - x1)
    #
    # b0 = y0
    # b1 = m1
    # b2 = (m2 - m1) / (x2 - x0)
    #
    # y = b0 + b1 * (x - x0) + b2 * (x - x0) * (x - x1)
    #
    # error = None
    # if x3 is not None and y3 is not None:
    #     d01 = (y1 - y0) / (x1 - x0)
    #     d12 = (y2 - y1) / (x2 - x1)
    #     d012 = (d12 - d01) / (x2 - x0)
    #     d123 = ((y3 - y2) / (x3 - x2) - d12) / (x3 - x1)
    #     d0123 = (d123 - d012) / (x3 - x0)
    #     error = error_estimado_interpolacion(d0123, [x0, x1, x2], x)
    #
    # return y, error
    raise NotImplementedError("Completa interpolacion_cuadratica")


if __name__ == "__main__":
    # nodos (0,1), (1,3), (2,7); evaluar en 1.5  ->  (4.75, None)
    print(interpolacion_cuadratica(0, 1, 1, 3, 2, 7, 1.5))
    # con cuarto dato: además del valor, el error estimado
    print(interpolacion_cuadratica(0, 1, 1, 3, 2, 7, 1.5, x3=3, y3=13))
