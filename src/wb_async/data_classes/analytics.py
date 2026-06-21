from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetTasksResponseData:
    id: int
    status: Literal['new', 'processing', 'done', 'purged', 'canceled']


@dataclass(frozen=True, slots=True)
class WarehouseInfo:
    warehouseName: str
    quantity: int


@dataclass(frozen=True, slots=True)
class WarehouseRemainsResult:
    brand: str
    subjectName: str
    vendorCode: str
    nmId: int
    barcode: str
    techSize: str
    volume: float
    warehouses: list[WarehouseInfo]


@dataclass(frozen=True, slots=True)
class ExciseReportItem:
    name: str
    price: float | int
    currency_name_short: str
    excise_short: str
    barcode: str
    nm_id: int
    operation_type_id: int
    fiscal_doc_number: int
    fiscal_dt: str
    fiscal_drive_number: str
    rid: int
    srid: str


@dataclass(frozen=True, slots=True)
class MeasurementPenaltyItem:
    nmId: int
    subjectName: str
    dimId: int
    prcOver: float
    volume: float
    width: int
    length: int
    height: int
    volumeSup: float
    widthSup: int
    lengthSup: int
    heightSup: int
    photoUrls: list[str]
    dtBonus: str
    isValid: bool
    isValidDt: str
    reversalAmount: float
    penaltyAmount: float


@dataclass(frozen=True, slots=True)
class MeasurementPenalty:
    reports: list[MeasurementPenaltyItem]
    total: int


@dataclass(frozen=True, slots=True)
class WarehouseMeasurementItem:
    nmId: int
    subjectName: str
    dimId: int
    volume: float
    width: int
    length: int
    height: int
    photoUrls: list[str]
    dt: str


@dataclass(frozen=True, slots=True)
class WarehouseMeasurements:
    reports: list[WarehouseMeasurementItem]
    total: int


@dataclass(frozen=True, slots=True)
class DeductionsItem:
    dtBonus: str
    nmId: int
    oldShkId: int
    oldColor: str
    oldSize: str
    oldSku: str
    oldVendorCode: str
    newShkId: int
    newColor: str
    newSize: str
    newSku: str
    newVendorCode: str
    bonusSumm: float
    bonusType: str
    photoUrls: list[str]


@dataclass(frozen=True, slots=True)
class Deductions:
    reports: list[DeductionsItem]
    total: int


@dataclass(frozen=True, slots=True)
class AntifraudDetails:
    nmID: str
    sum: int
    currency: str
    dateFrom: str
    dateTo: str


@dataclass(frozen=True, slots=True)
class GoodsLabeling:
    amount: float
    date: str
    incomeId: int
    nmID: int
    photoUrls: list[str]
    shkID: int
    sku: str


@dataclass(frozen=True, slots=True)
class AcceptanceReport:
    count: int
    giCreateDate: str
    incomeId: int
    nmID: int
    shkCreateDate: str
    subjectName: str
    total: float


@dataclass(frozen=True, slots=True)
class PaidStorageReport:
    date: str
    logWarehouseCoef: float
    number: int
    officeId: int
    warehouse: str
    warehouseCoef: float
    giId: int
    chrtId: int
    size: str
    barcode: str
    subject: str
    brand: str
    vendorCode: str
    nmId: int
    volume: float
    calcType: str
    warehousePrice: float
    barcodesCount: int
    palletPlaceCode: int
    palletCount: float
    originalDate: str
    loyaltyDiscount: float
    tariffFixDate: str
    tariffLowerDate: str


@dataclass(frozen=True, slots=True)
class RegionSale:
    cityName: str
    countryName: str
    foName: str
    nmID: int
    regionName: str
    sa: str
    saleInvoiceCostPrice: float
    saleInvoiceCostPricePerc: float
    saleItemInvoiceQty: int


@dataclass(frozen=True, slots=True)
class BrandShareParentSubject:
    parrentId: int
    parrentNmae: str


@dataclass(frozen=True, slots=True)
class BrandShare:
    applyDate: str
    brandRating: int
    pricePercent: float
    qtyPercent: float


@dataclass(frozen=True, slots=True)
class BannedProductsBlocked:
    brand: str
    nmId: int
    title: str
    vendorCode: str
    reason: str


@dataclass(frozen=True, slots=True)
class BannedProductsShadowed:
    brand: str
    nmId: int
    title: str
    vendorCode: str
    nmRating: float | int


@dataclass(frozen=True, slots=True)
class GoodsReturn:
    barcode: str
    brand: str
    completedDt: str | None
    dstOfficeAddress: str
    dstOfficeId: int
    expiredDt: str | None
    isStatusActive: int
    nmId: int
    orderDt: str
    orderId: int
    readyToReturnDt: str | None
    reason: str
    returnType: str
    shkId: int
    srid: str
    status: str
    stickerId: str
    subjectName: str
    techSize: str


@dataclass(frozen=True, slots=True)
class SalesFunnelProduct:
    pass
