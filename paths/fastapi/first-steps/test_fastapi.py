import pytest
from fastapi.testclient import TestClient
from main import app
from main import SocieType
from main import Product


def test_root():
    # Setup
    client = TestClient(app)
    # Exercise
    response = client.get("/")
    # Verify
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize("item_id, expected_code", [(3, 200), ("foo", 422)])
def test_read_item(item_id, expected_code):
    # Setup
    client = TestClient(app)
    # Exercise
    response = client.get(f"/items/{item_id}")
    # Verify
    assert response.status_code == expected_code
    if item_id == 3:
        assert response.json() == {"item_id": 3}
    else:
        assert not response.json() == {"item_id": 3}


@pytest.mark.parametrize(
    "socie_type, socie_description",
    [
        (SocieType.humane, "Socie Productor"),
        (SocieType.adherente, "Socie Consumidor"),
        (SocieType.proveedor, "No Socie"),
    ]
)
def test_read_socie_types_happy_path(socie_type, socie_description):
    # Setup
    client = TestClient(app)
    # Exercise
    response = client.get(f"/socies_types/{socie_type.value}")

    # Verify
    assert response.status_code == 200
    assert response.json() == {"socie type": socie_type.value, "Socie description": socie_description}


def test_create_product():
    # Setup
    client = TestClient(app)
    producto = Product(
        name="cerveza",
        price=10.0,
        description='Cerveza de la huerta',
        tax=21.0,
    )
    # Exercise
    response = client.post("/create_product/", json=producto.model_dump())

    # Verify
    assert response.status_code == 200
    assert response.json() == producto.model_dump()
