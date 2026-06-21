from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Office:
    address: str
    name: str
    city: str
    id: int
    longitude: float
    latitude: float
    cargo_type: int
    delivery_type: int
    federal_district: str | None
    selected: bool


@dataclass(frozen=True, slots=True)
class Warehouse:
    name: str
    office_id: int
    id: int
    cargo_type: int
    delivery_type: int
    is_deleting: bool
    is_processing: bool


@dataclass(frozen=True, slots=True)
class WarehouseContract:
    comment: str
    phone: str


@dataclass(frozen=True, slots=True)
class WarehouseStock:
    chrtId: int
    amount: int
