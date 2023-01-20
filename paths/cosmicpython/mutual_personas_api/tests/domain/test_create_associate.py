import pytest
from decimal import Decimal
import uuid
from mutual_personas.domain.socies import Socie, Cuote
from datetime import datetime, timedelta

@pytest.fixture
def new_socie(*args):
    id= 1
    nombre = "Pepe"
    apellido = "Del Rio"
    dni = 27890098
    email = "unemail@personas.com"
    telefono = "+54115555555"
    direccion="una direccion"
    codigo_postal = "un codigo con 1234"
    tipo_de_socio= 1
    uuid_number = str(uuid.uuid1())


    return Socie(id, nombre, apellido, dni, email, telefono, direccion, codigo_postal, tipo_de_socio, uuid_number)


def test_new_socie(new_socie):

    # Given
    a_socie=new_socie

    # Then
    assert isinstance(a_socie, Socie)


def test_add_payed_actual_cuote_and_is_activated(new_socie):
    # Given
    now = datetime.now()
    a_socie = new_socie
    a_cuote = Cuote(now, Decimal(10.00))
    another_cuote = Cuote(now - timedelta(days=31), Decimal(10.00))
    cuotes=[a_cuote, another_cuote]
    # When
    a_socie.pay_cuotes(cuotes)
    # Then
    # There is same ammounts of cuotes in propertie cuotes than pay_cuotes
    assert len(a_socie.cuotes) == len(cuotes)
    assert a_socie.cuotes ==set(cuotes)
    # the activated propertie is true
    assert a_socie.activated

def test_socie_has_older_cuotes_but_is_inactive(new_socie):
    # Given
    now = datetime.now()
    a_socie = new_socie
    a_cuote = Cuote(now - timedelta(days=61), Decimal(10.00))
    another_cuote = Cuote(now - timedelta(days=31), Decimal(10.00))
    cuotes=[a_cuote, another_cuote]
    # When
    a_socie.pay_cuotes(cuotes)
    # Then
    # There is same ammounts of cuotes in propertie cuotes than pay_cuotes
    assert len(a_socie.cuotes) == len(cuotes)
    assert a_socie.cuotes ==set(cuotes)
    # the activated propertie is false
    assert not a_socie.activated


def socie_is_not_activated():
    pass
