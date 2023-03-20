from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol

class Pricing(Protocol):
    def get_total_price(self) -> int:
        ... # Computate de total price for rental

class PricePerDay:
    price_per_day: int
    nro_of_days: int

    def get_total_price(self) -> int:
        return self.price_per_day * self.nro_of_days


class PricePerKm:
    price_per_km: int
    nro_of_km: int

    def get_total_price(self) -> int:
        return self.price_per_km * self.nro_of_km


class PricePerMonth:
    price_per_month: int
    nro_of_month: int

    def get_total_price(self) -> int:
        return self.price_per_month * self.nro_of_month

class FuelType(Enum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()


class TruckCabStyle(Enum):
    REGULAR = auto()
    EXTENDED = auto()
    CREW = auto()


@dataclass
class Vehicle:
    brand: str
    model: str
    color: str
    fuel_type: FuelType
    license_plate: str
    reserved: bool
    pricing: list[Pricing] = field(default_factory=list)


@dataclass
class Car(Vehicle):
    number_of_seats: int = 5
    storage_capacity_litres: int = 200


@dataclass
class Truck(Vehicle):
    cab_style: TruckCabStyle = TruckCabStyle.REGULAR


@dataclass
class Trailer:
    brand: str
    model: str
    capacity_m3: int
    reserved: bool
    pricing: list[Pricing] = field(default_factory=list)


def main():
    pass


if __name__ == "__main__":
    main()
