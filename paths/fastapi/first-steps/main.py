from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from decimal import Decimal
class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class SocieType(str, Enum):
    humane = "Humane"
    adherente = "Adherente"
    proveedor = "Proveedor"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

@app.get("/socies_types/{socie_type}")
async def get_socies_type(socie_type: SocieType):
    if socie_type is SocieType.humane:
        return {"socie type": socie_type, "Socie description": "Socie Productor"}

    if socie_type is SocieType.adherente:
        return {"socie type": socie_type, "Socie description": "Socie Consumidor"}


    return {"socie type": socie_type, "Socie description": "No Socie"}


@app.post("/create_product/")
async def create_product(product: Product):
    return product
