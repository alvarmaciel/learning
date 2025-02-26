from dataclasses import dataclass
from datetime import date

class OutOfStock(Exception):
    pass

@dataclass(frozen=True)
class LineItem:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(self, ref: str, sku: str, quantity: int, eta: date | None):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations: set[LineItem] = set()

    def __eq__(self, other):
        """ Will be equal only if is a Batch Object and has the same reference
        """
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return False
        return self.eta > other.eta

    def allocate(self, order_line_item: LineItem) -> None:
        if self.can_allocate(order_line_item):
            self._allocations.add(order_line_item)

    def deallocate(self, order_line_item: LineItem) -> None:
        if order_line_item in self._allocations:
            self._allocations.remove(order_line_item)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, order_line_item: LineItem) -> bool:
        return self.sku == order_line_item.sku and self.available_quantity >= order_line_item.quantity


def allocate(line: LineItem, batches: [Batch]) -> str:
    try:
        batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))

        batch.allocate(line)
        return batch.reference
    except StopIteration as e:

        raise OutOfStock(f"Out of stock for sku: {line.sku}")
