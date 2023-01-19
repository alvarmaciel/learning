import uuid
from random import randint
class Socies:
    def __int__(self,
                nombre: str,
                apellido:str,
                dni: int,
                email: str,
                telefono: str,
                direccion: str,
                codigo_postal: str,
                tipo_de_socio: int,
                nro_uuid: uuid = None,
                nro: int =None,
                ):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.tipo_de_socio = tipo_de_socio
        self.nro_uuid: nro_uuid if nro_uuid is not None else uuid.uuid1()
        self.nro_de_socio = nro if nro is not None else randint(1,1000)




