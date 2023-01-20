import pytest
import uuid
from mutual_personas.domain.socies import Socie

def test_add_socie():
    """Variables de instancia de los socies
        - Nombre
        - Apellido
        - DNI
        - Nro de socie: Automatico
        - Email
        - Teléfono
        - Dirección
        - Codigo Postal
        - tipo de Socio: Pleno(1) o General(0)
        - Numero de socios: automático correlativo.
        - uuid: clave única
    """
    # Given
    nombre = "Pepe"
    apellido = "Del Rio"
    dni = 27890098
    email = "unemail@personas.com"
    telefono = "+54115555555"
    direccion="una direccion"
    codigo_postal = "un codigo con 1234"
    tipo_de_socio= 1
    uuid_number = uuid.uuid1()

    # When
    nuevo_socie = Socie(nombre, apellido, dni, email, telefono, direccion, codigo_postal, tipo_de_socio, uuid_number)

    # Then
    assert nuevo_socie.nombre == nombre
    assert nuevo_socie.apellido == apellido
    assert nuevo_socie.dni == dni
    assert isinstance(nuevo_socie.nro_de_socie, int)
    assert nuevo_socie.email == email
    assert nuevo_socie.telefono == telefono
    assert nuevo_socie.direccion == direccion
    assert nuevo_socie.codigo_postal == codigo_postal
    assert nuevo_socie.tipo_de_socio == tipo_de_socio
    assert isinstance(nuevo_socie.nro_uuid, uuid.UUID)
