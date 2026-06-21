from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Balance:
    currency: str
    current: float
    for_withdraw: float


@dataclass(frozen=True, slots=True)
class ReportDetailByPeriod:
    realizationreport_id: int
    date_from: str
    date_to: str
    create_dt: str
    currency_name: str
    suppliercontract_code: dict | None = None
    rrd_id: int = 0
    gi_id: int = 0
    dlv_prc: float = 0
    fix_tariff_date_from: str = "2026-01-01"
    fix_tariff_date_to: str = "2026-01-01"
    subject_name: str =  "Предмет"
    nm_id: int = 0
    brand_name: str = "Бренд"
    sa_name: str = "Артикул продавца"
    ts_name: str = "0"
    barcode: str = "Баркод"
    doc_type_name: str = "Продажа"
    quantity: int = 1
    retail_price: float | int = 0
    retail_amount: int = 0
    sale_percent: float | int = 0
    commission_percent: float | int = 0
    office_name: str = "Склад"
    supplier_oper_name: str = "Обоснование для оплаты"
    order_dt: str = "2026-01-01T00:00:00Z"
    sale_dt: str = "2026-01-01T00:00:00Z"
    rr_dt: str = "2026-01-01"
    shk_id: int = 1234567890
    retail_price_withdisc_rub: float | int = 0
    delivery_amount: int = 0
    return_amount: int = 0
    delivery_rub: int = 0
    gi_box_type_name: str = "Тип коробов"
    product_discount_for_report: int = 0
    supplier_promo: int = 0
    ppvz_spp_prc: float | int = 0
    ppvz_kvw_prc_base: float | int = 0
    ppvz_kvw_prc: float | int = 0
    sup_rating_prc_up: int = 0
    is_kgvp_v2: int = 0
    ppvz_sales_commission: float | int = 23.74
    ppvz_for_pay: float | int = 376.99
    ppvz_reward: int = 0
    acquiring_fee: float | int = 14.89
    acquiring_percent: float | int = 4.06
    payment_processing: str = "Комиссия за организацию платежа с НДС"
    acquiring_bank: str = "Тинькофф"
    ppvz_vw: float | int = 22.25
    ppvz_vw_nds: float | int = 4.45
    ppvz_office_name: str = "Пункт самовывоза (ПВЗ)"
    ppvz_office_id: int = 105383
    ppvz_supplier_id: int = 186465
    ppvz_supplier_name: str = "ИП Жасмин"
    ppvz_inn: str = "010101010101"
    declaration_number: str = ""
    bonus_type_name: str = "Штраф МП. Невыполненный заказ (отмена клиентом после недовоза)"
    sticker_id: str = "1964038895"
    site_country: str = "Россия"
    srv_dbs: bool = True
    penalty: float | int = 231.35
    additional_payment: int = 0
    rebill_logistic_cost: float | int = 1.349
    rebill_logistic_org: str = "ИП Иванов Иван Иванович(123456789012)"
    storage_fee: float | int = 12647.29
    deduction: int = 6354
    acceptance: int = 865
    assembly_id: int = 2816993144
    kiz: str = "0102900000376311210G2CIS?ehge)S\u001d91002A\u001d92F9Qof4FDo/31Icm14kmtuVYQzLypxm3HWkC1vQ/+pVVjm1dNAth1laFMoAGn7yEMWlTjxIe7lQnJqZ7TRZhlHQ=="
    srid: str = "0f1c3999172603062979867564654dac5b702849"
    report_type: int = 1
    is_legal_entity: bool = False
    trbx_id: str = "WB-TRBX-1234567"
    installment_cofinancing_amount: int = 0
    wibes_wb_discount_percent: int = 1
    cashback_amount: int = 0
    cashback_discount: int = 0
    cashback_commission_change: int = 0
    order_uid: str = "id375f16c4bec295d9995393af803ff7b"
    payment_schedule: int = 0
    delivery_method: str = "FBS, (МГТ)"
    seller_promo_id: int = 14350
    seller_promo_discount: int = 0
    loyalty_id: int = 0
    loyalty_discount: int = 0
    uuid_promocode: str = ""
    sale_price_promocode_discount_prc: int = 0


@dataclass(frozen=True, slots=True)
class SupplierStockItem:
    lastChangeDate: str
    warehouseName: str
    supplierArticle: str
    nmId: int
    barcode: str
    quantity: int
    inWayToClient: int
    inWayFromClient: int
    quantityFull: int
    category: str
    subject: str
    brand: str
    techSize: str
    price: float
    discount: float
    isSupply: bool
    isRealization: bool
    scCode: str


@dataclass(frozen=True, slots=True)
class SupplierOrderItem:
    date: str
    lastChangeDate: str
    warehouseName: str
    warehouseType: str
    countryName: str
    oblastOkrugName: str
    regionName: str
    supplierArticle: str
    nmId: int
    barcode: str
    category: str
    subject: str
    brand: str
    techSize: str
    incomeID: int
    isSupply: bool
    isRealization: bool
    totalPrice: float
    discountPercent: int
    spp: float
    finishedPrice: float
    priceWithDisc: float
    isCancel: bool
    cancelDate: str
    sticker: str
    gNumber: str
    srid: str


@dataclass(frozen=True, slots=True)
class SupplierSalesItem:
    date: str
    lastChangeDate: str
    warehouseName: str
    warehouseType: str
    countryName: str
    oblastOkrugName: str
    regionName: str
    supplierArticle: str
    nmId: int
    barcode: str
    category: str
    subject: str
    brand: str
    techSize: str
    incomeID: int
    isSupply: bool
    isRealization: bool
    totalPrice: float
    discountPercent: int
    spp: float
    finishedPrice: float
    priceWithDisc: float
    isCancel: bool
    cancelDate: str
    sticker: str
    gNumber: str
    srid: str
