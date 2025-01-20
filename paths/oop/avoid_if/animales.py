from abc import ABC, abstractmethod


class Animales(ABC):

    @abstractmethod
    def hablar(self):
        pass

class Perro(Animales):

    def hablar(self):
        return "Guau"

class Gato(Animales):

    def hablar(self):
        return "Miau"

class Pajaro(Animales):

    def hablar(self):
        return "Pío"
