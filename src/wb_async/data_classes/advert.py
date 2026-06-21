from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Literal


@dataclass(frozen=True, slots=True)
class Timestamps:
    created: datetime
    updated: datetime
    started: datetime
    deleted: datetime


@dataclass(frozen=True, slots=True)
class Company:
    advertId: int
    changeTime: datetime


@dataclass(frozen=True, slots=True)
class Advert:
    type: int
    status: int
    count: int
    advertList: Tuple[Company]


@dataclass(frozen=True, slots=True)
class Adverts:
    adverts: list[Advert]
    all: int


@dataclass(frozen=True, slots=True)
class BidKopeck:
    search: int
    recommendations: int


@dataclass(frozen=True, slots=True)
class Subject:
    id: int
    name: str


@dataclass(frozen=True, slots=True)
class NMSettings:
    bid_kopecks: BidKopeck
    subject: Subject
    nm_id: int


@dataclass(frozen=True, slots=True)
class Placements:
    search: bool
    recommendations: bool


@dataclass(frozen=True, slots=True)
class AdvertSettings:
    payment_type: Literal['cpm', 'cpc']
    name: str
    placements: Placements


@dataclass(frozen=True, slots=True)
class CompanyAdvertInfo:
    bid_type: Literal['unified', 'manual']
    id: int # id компании
    nm_settings: Tuple[NMSettings]
    settings: AdvertSettings
    status: int
    timestamps: Timestamps


@dataclass(frozen=True, slots=True)
class CompanyInfo:
    adverts: Tuple[CompanyAdvertInfo]


@dataclass(frozen=True, slots=True)
class Cashback:
    sum: int
    percent: int
    expiration_date: str # ISO 8601


@dataclass(frozen=True, slots=True)
class Balance:
    balance: int # рублях
    net: int
    bonus: int
    cashback: Tuple[Cashback]


@dataclass(frozen=True, slots=True)
class CompanyCache:
    cash: int
    netting: int
    total: int


@dataclass(frozen=True, slots=True)
class CostHistory:
    updNum: int
    updTime: str | None
    updSum: int
    advertId: int
    campName: str
    advertType: int
    paymentType: str
    advertStatus: int


@dataclass(frozen=True, slots=True)
class Payments:
    id: int
    date: str
    sum: int
    type: int
    statusId: int
    cardStatus: int
