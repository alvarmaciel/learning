from abc import ABC, abstractmethod


class Figura(ABC):

    @abstractmethod
    def area(self) -> int:
        pass


class Circulo(Figura):
    def __init__(self, radio:int):
        self.radio = radio

    def area(self):
        return self.radio * 3.14


class Cuadrado(Figura):
    def __init__(self, lado:int):
        self.lado = lado

    def area(self):
        return self.lado * 2

class Triangulo(Figura):
    def __init__(self, base:int, altura:int):
        self.base = base
        self.altura = altura

    def area(self):
        return (self.base * self.altura)/2
