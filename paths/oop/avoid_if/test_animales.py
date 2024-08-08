import pytest
from animales import Perro, Gato, Pájaro

"""
Crea una jerarquía de clases para representar diferentes tipos de animales: Perro, Gato y Pájaro.
Cada clase debe implementar un método hablar() que devuelva el sonido característico del animal.
Usa polimorfismo para evitar estructuras if al llamar al método hablar de una lista de animales.
"""

def test_hablar_perro():
    perro = Perro()
    assert perro.hablar() == "Guau"

def test_hablar_gato():
    gato = Gato()
    assert gato.hablar() == "Miau"

def test_hablar_pajaro():
    pajaro = Pájaro()
    assert pajaro.hablar() == "Pío"

def test_hablar_varios_animales():
    animales = [Perro(), Gato(), Pájaro()]
    sonidos = [animal.hablar() for animal in animales]
    assert sonidos == ["Guau", "Miau", "Pío"]
