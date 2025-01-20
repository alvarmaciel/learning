from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class LineItem:
    order_id: str
    sku: str
    quantity: int

class Batch:
    def __init__(self, batch_id:str, sku:str, quantity:int, eta:date):
        self.batch_id = batch_id
        self.sku = sku
        self.quantity = quantity
        self.eta = eta

    def allocate(self, order_line_item: LineItem) -> None:
        self.quantity -= order_line_item.quantity
