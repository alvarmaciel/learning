import pytest
from .figuras import Circulo, Cuadrado, Triangulo

"""
Crea una jerarquía de clases para representar diferentes figuras geométricas: Círculo, Cuadrado y Triángulo.
Cada clase debe implementar un método area() que devuelva el área de la figura.
Usa polimorfismo para evitar estructuras if al calcular el área de una lista de figuras.
"""


def test_area_circulo():
    circulo = Circulo(1)
    assert pytest.approx(circulo.area(), 0.01) == 3.14

def test_area_cuadrado():
    cuadrado = Cuadrado(2)
    assert cuadrado.area() == 4

def test_area_triangulo():
    triangulo = Triangulo(3, 4)
    assert triangulo.area() == 6

def test_area_varias_figuras():
    figuras = [Circulo(1), Cuadrado(2), Triangulo(3, 4)]
    areas = [figura.area() for figura in figuras]
    assert pytest.approx(areas[0], 0.01) == 3.14
    assert areas[1] == 4
    assert areas[2] == 6
