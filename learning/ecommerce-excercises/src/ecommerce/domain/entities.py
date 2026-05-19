from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import partial

@dataclass
class Product:
    name: str
    category: str
    price_cents: int
    stock: int
    created_at: datetime = field(default_factory=partial(datetime.now, UTC))
