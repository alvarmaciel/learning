from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, List
import uuid
from random import randint
from dataclasses import dataclass

@dataclass(frozen=True)
class Cuote:
    date:datetime
    amount:Decimal


class Socie:
    def __init__(self,
                id: int,
                nombre: str,
                apellido:str,
                dni: int,
                email: str,
                telefono: str,
                direccion: str,
                codigo_postal: str,
                tipo_de_socio: int,
                nro_uuid: str,
                ):
        self.ide = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.tipo_de_socio = tipo_de_socio
        self.nro_uuid= nro_uuid
        self.cuotes=set()

    @property
    def activated(self)-> bool:
        current_month = datetime.now().strftime('%m')
        current_year_full = datetime.now().strftime('%Y')
        if not self.cuotes:
            return False
        for cuote in self.cuotes:
            if cuote.date.strftime('%Y')==current_year_full and cuote.date.strftime('%m') == current_month:
                return True
        return False


    def pay_cuotes(self, cuotes:List[Cuote]):
        current_month = datetime.now().strftime('%m')
        current_year_full = datetime.now().strftime('%Y')
        for cuote in cuotes:
            self.cuotes.add(cuote)
