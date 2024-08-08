import pytest
from empleados import Gerente, Desarrollador, Diseñador

"""
Crea una jerarquía de clases para representar diferentes tipos de empleados: Gerente, Desarrollador y Diseñador.
Cada clase debe implementar un método generar_reporte() que devuelva un reporte específico del empleado.
Usa polimorfismo para evitar estructuras if al generar reportes de una lista de empleados.
"""


def test_generar_reporte_gerente():
    gerente = Gerente()
    assert gerente.generar_reporte() == "Reporte de Gerente"

def test_generar_reporte_desarrollador():
    desarrollador = Desarrollador()
    assert desarrollador.generar_reporte() == "Reporte de Desarrollador"

def test_generar_reporte_diseñador():
    diseñador = Diseñador()
    assert diseñador.generar_reporte() == "Reporte de Diseñador"

def test_generar_varios_reportes():
    empleados = [Gerente(), Desarrollador(), Diseñador()]
    reportes = [empleado.generar_reporte() for empleado in empleados]
    assert reportes == [
        "Reporte de Gerente",
        "Reporte de Desarrollador",
        "Reporte de Diseñador"
    ]
