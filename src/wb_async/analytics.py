from typing import Literal

from core.requests_makers.asyncio_limiter import WindowRateLimiter
from .base import WbBaseService
from .data_classes import analytics, globals

from .settings import Settings


class AnalyticsService(WbBaseService):
    def __init__(self, token: str):
        super().__init__(
            base_url=Settings.WB_ANALYTICS_URL,
            token=token,
        )

    # Раздел отчеты
    @WindowRateLimiter(max_calls=1, time_window=60)
    async def warehouse_remains_get_task_id(
        self,
        locale: globals.Locale = 'ru',
        group_by_brand: bool = False,
        group_by_subject: bool = False,
        group_by_sa: bool = False,
        group_by_nm: bool = False,
        group_by_barcode: bool = False,
        group_by_size: bool = False,
        filter_pics: int = 0,
        filter_volume: int = 0,
    ) -> int | None:
        """
        Метод создаёт задание на генерацию отчёта об остатках на складах WB.
        Параметры groupBy и filter (группировки и фильтры) можно задать в любой комбинации — аналогично версии в личном кабинете.
        """
        ans = await self.get('/v1/warehouse_remains', params={
            'locale': locale,
            'groupByBrand': group_by_brand,
            'groupBySubject': group_by_subject,
            'groupBySa': group_by_sa,
            'groupByNm': group_by_nm,
            'groupByBarcode': group_by_barcode,
            'groupBySize': group_by_size,
            'filterPics': filter_pics,
            'filterVolume': filter_volume,
        })
        if ans.status == 200:
            return ans.json['data']['taskId']

    @WindowRateLimiter(max_calls=1, time_window=5)
    async def warehouse_remains_status(
        self,
        task_id: int,
    ) -> analytics.GetTasksResponseData | None:
        """
        Метод возвращает статус задания на генерацию отчёта об остатках на складах WB.
        """
        ans = await self.get(f'/v1/warehouse_remains/tasks/{task_id}/status')
        if ans.status == 200:
            return analytics.GetTasksResponseData(**ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def warehouse_remains_get(
        self,
        task_id: int,
    ) -> tuple[analytics.WarehouseRemainsResult, ...] | None:
        """
        Метод возвращает отчёт об остатках на складах WB по ID задания на генерацию.
        """
        ans = await self.get(f'/v1/warehouse_remains/tasks/{task_id}/download')
        if ans.status == 200:
            return tuple(analytics.WarehouseRemainsResult(**item) for item in ans.json['data'])
        elif ans.status == 204:
            return tuple()

    @WindowRateLimiter(max_calls=10, time_window=30)
    async def excise_report(
        self,
        date_from: str,
        date_to: str,
        countries: list[globals.Country] | None = None,
    ) -> tuple[analytics.ExciseReportItem, ...] | None:
        """
        Метод возвращает отчёт с операциями по товарам с обязательной маркировкой.
        """
        params = {
            'dateFrom': date_from,
            'dateTo': date_to,
        }
        json_data = {}
        if countries is not None:
            json_data['countries'] = countries
        ans = await self.post(
            '/v1/analytics/excise-report',
            params=params,
            json=json_data
        )
        if ans.status == 200:
            return tuple(
                analytics.ExciseReportItem(**item) for item in ans.json['response']['data']
            )

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def measurement_penalties(
        self,
        date_from: str,
        date_to: str,
        limit: int = 1000,
        offset: int = 0,
    ) -> analytics.MeasurementPenalty | None:
        """
        Метод возвращает отчёт об удержаниях за занижение габаритов упаковки
        """
        ans = await self.get(
            '/v1/measurement-penalties',
            params={
                'dateFrom': date_from,
                'dateTo': date_to,
                'limit': limit,
                'offset': offset,
            }
        )
        if ans.status == 200:
            return analytics.MeasurementPenalty(**ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def warehouse_measurements(
        self,
        date_from: str,
        date_to: str,
        limit: int = 1000,
        offset: int = 0,
    ) -> analytics.WarehouseMeasurements | None:
        """
        Метод возвращает отчёт с операциями по товарам с обязательной маркировкой.
        """
        ans = await self.get(
            '/v1/warehouse-measurements',
            params={
                'dateFrom': date_from,
                'dateTo': date_to,
                'limit': limit,
                'offset': offset,
            }
        )
        if ans.status == 200:
            return analytics.WarehouseMeasurements(**ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def deductions(
        self,
        date_from: str,
        date_to: str,
        sort: Literal['nmId', 'dtBonus', 'bonusSumm'] = 'nmId',
        order: Literal['asc', 'desc'] = 'desc',
        limit: int = 1000,
        offset: int = 0,
    ) -> analytics.Deductions | None:
        """
        Метод возвращает отчёт об удержаниях за подмены и неверные вложения
        """
        ans = await self.get(
            '/v1/deductions',
            params={
                'dateFrom': date_from,
                'dateTo': date_to,
                'sort': sort,
                'order': order,
                'limit': limit,
                'offset': offset,
            }
        )
        if ans.status == 200:
            return analytics.Deductions(**ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=10*60)
    async def antifraud_details(
        self,
        data: str | None = None
    ) -> tuple[analytics.AntifraudDetails, ...] | None:
        """
        Метод возвращает отчёт об удержаниях за самовыкупы. Отчёт формируется каждую неделю по средам, до 7:00 по московскому времени, и содержит данные за одну неделю.
        Удержание за самовыкуп — 30% от стоимости товаров.
        Минимальная сумма всех удержаний — 100 000 ₽, если за неделю в ПВЗ привезли ваших товаров больше, чем на сумму 100 000 ₽.
        Данные доступны с августа 2023.
        """
        params = {}
        if data is not None:
            params['data'] = data
        ans = await self.get(
            '/v1/analytics/antifraud-details',
            params=params
        )
        if ans.status == 200:
            return tuple(analytics.AntifraudDetails(**item) for item in ans.json['details'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def goods_labeling(
        self,
        date_from: str,
        date_to: str,
    ) -> tuple[analytics.GoodsLabeling, ...] | None:
        """
        Метод возвращает отчёт о штрафах за отсутствие обязательной маркировки товаров.
        В отчёте представлены фотографии товаров, на которых маркировка отсутствует либо не считывается.
        Можно получить данные максимум за 31 день. Данные доступны с марта 2024.
        """
        ans = await self.get(
            '/v1/analytics/goods-labeling',
            params={
                'dateFrom': date_from,
                'dateTo': date_to,
            }
        )
        if ans.status == 200:
            return tuple(analytics.GoodsLabeling(**item) for item in ans.json['report'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def acceptance_report_get_task_id(
        self,
        date_from: str,
        date_to: str,
    ) -> int | None:
        """
        Метод создаёт задание на генерацию отчёта об операциях при приёмке.
        """
        ans = await self.get('/v1/acceptance_report', params={
            'dateFrom': date_from,
            'dateTo': date_to,
        })
        if ans.status == 200:
            return ans.json['data']['taskId']

    @WindowRateLimiter(max_calls=1, time_window=5)
    async def acceptance_report_status(
        self,
        task_id: int,
    ) -> analytics.GetTasksResponseData | None:
        """
        Метод возвращает статус задания на генерацию отчёта об операциях при приёмке.
        """
        ans = await self.get(f'/v1/acceptance_report/tasks/{task_id}/status')
        if ans.status == 200:
            return analytics.GetTasksResponseData(**ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def acceptance_report_get(
        self,
        task_id: int,
    ) -> tuple[analytics.AcceptanceReport, ...] | None:
        """
        Метод возвращает отчёт об операциях при приёмке по ID задания на генерацию.
        """
        ans = await self.get(f'/v1/warehouse_remains/tasks/{task_id}/download', params={
            'taskId': task_id,
        })
        if ans.status == 200:
            return tuple(analytics.AcceptanceReport(**item) for item in ans.json['data'])
        elif ans.status == 204:
            return tuple()

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def paid_storage_get_task_id(
        self,
        date_from: str,
        date_to: str,
    ) -> int | None:
        """
        Метод создаёт задание на генерацию отчёта об операциях при приёмке.
        """
        ans = await self.get('/v1/paid_storage', params={
            'dateFrom': date_from,
            'dateTo': date_to,
        })
        if ans.status == 200:
            return ans.json['data']['taskId']

    @WindowRateLimiter(max_calls=1, time_window=5)
    async def paid_storage_status(
        self,
        task_id: int,
    ) -> analytics.GetTasksResponseData | None:
        """
        Метод возвращает статус задания на генерацию отчёта об операциях при приёмке.
        """
        ans = await self.get(f'/v1/paid_storage/tasks/{task_id}/status')
        if ans.status == 200:
            return analytics.GetTasksResponseData(**ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def paid_storage_get(
        self,
        task_id: int,
    ) -> tuple[analytics.PaidStorageReport, ...] | None:
        """
        Метод возвращает отчёт об операциях при приёмке по ID задания на генерацию.
        """
        ans = await self.get(f'/v1/paid_storage/tasks/{task_id}/download', params={
            'taskId': task_id,
        })
        if ans.status == 200:
            return tuple(analytics.PaidStorageReport(**item) for item in ans.json['data'])
        elif ans.status == 204:
            return tuple()

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def region_sale(
        self,
        date_from: str,
        date_to: str,
    ) -> tuple[analytics.RegionSale, ...] | None:
        """
        Метод возвращает отчёт с данными продаж, сгруппированных по регионам стран.
        Можно получить отчёт максимум за 31 день.
        """
        ans = await self.get('/v1/analytics/region-sale', params={
            'dateFrom': date_from,
            'dateTo': date_to,
        })
        if ans.status == 200:
            return tuple(analytics.RegionSale(**item) for item in ans.json['report'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def brand_share_brands(
        self,
    ) -> tuple[str, ...] | None:
        """
        Метод возвращает список брендов продавца для отчёта о доле бренда в продажах.
        Можно получить только бренды, которые:
        Продавались за последние 90 дней.
        Есть на складе WB.
        """
        ans = await self.get('/v1/analytics/brand-share/brands', params={
        })
        if ans.status == 200:
            return tuple(ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=5)
    async def brand_share_parent_subject(
        self,
        brand: str,
        date_from: str,
        date_to: str,
        locale: globals.Locale = 'ru',
    ) -> tuple[analytics.BrandShareParentSubject, ...] | None:
        """
        Метод возвращает родительские категории бренда продавца для отчёта о доле бренда в продажах.
        Можно получить отчёт максимум за 365 дней. Данные доступны с 1 ноября 2022.
        """
        ans = await self.get('/v1/analytics/brand-share/parent-subjects', params={
            'dateFrom': date_from,
            'dateTo': date_to,
            'brand': brand,
            'locale': locale,
        })
        if ans.status == 200:
            return tuple(analytics.BrandShareParentSubject(**item) for item in ans.json['data'])

    @WindowRateLimiter(max_calls=1, time_window=5)
    async def brand_share(
        self,
        parent_id: int,
        brand: str,
        date_from: str,
        date_to: str,
    ) -> tuple[analytics.BrandShare, ...] | None:
        """
        Метод возвращает отчёт о доле бренда продавца в продажах.
        Можно получить отчёт максимум за 365 дней. Данные доступны с 1 ноября 2022.
        """
        ans = await self.get('/v1/analytics/brand-share', params={
            'dateFrom': date_from,
            'dateTo': date_to,
            'brand': brand,
            'parentId': parent_id,
        })
        if ans.status == 200:
            return tuple(analytics.BrandShare(**item) for item in ans.json['report'])

    @WindowRateLimiter(max_calls=1, time_window=10)
    async def banned_products_blocked(
        self,
        sort: Literal['brand', 'nmId', 'title', 'vendorCode', 'reason'] = 'nmId',
        order: globals.Order = 'desc',
    ) -> tuple[analytics.BannedProductsBlocked, ...] | None:
        """
        Метод возвращает список заблокированных карточек товаров продавца с причинами блокировки.
        """
        ans = await self.get('/v1/analytics/banned-products/blocked', params={
            'sort': sort,
            'order': order,
        })
        if ans.status == 200:
            return tuple(analytics.BannedProductsBlocked(**item) for item in ans.json['report'])

    @WindowRateLimiter(max_calls=1, time_window=10)
    async def banned_products_shadowed(
        self,
        sort: Literal['brand', 'nmId', 'title', 'vendorCode', 'reason'] = 'nmId',
        order: globals.Order = 'desc',
    ) -> tuple[analytics.BannedProductsShadowed, ...] | None:
        """
        Метод возвращает .
        """
        ans = await self.get('/v1/analytics/banned-products/shadowed', params={
            'sort': sort,
            'order': order,
        })
        if ans.status == 200:
            return tuple(analytics.BannedProductsShadowed(**item) for item in ans.json['report'])

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def goods_return(
        self,
        date_from: str,
        date_to: str,
    ) -> tuple[analytics.GoodsReturn, ...] | None:
        """
        Метод возвращает отчёт о возвратах товаров продавцу.
        Можно получить отчёт максимум за 31 день.
        """
        ans = await self.get('/v1/analytics/goods-return', params={
            'dateFrom': date_from,
            'dateTo': date_to,
        })
        if ans.status == 200:
            return tuple(analytics.GoodsReturn(**item) for item in ans.json['report'])

    # Раздел Аналитика и данные
    @WindowRateLimiter(max_calls=1, time_window=60)
    async def sales_funnel_products(
        self,
        selected_period_start: str,
        selected_period_end: str,
        past_period_start: str | None = None,
        past_period_end: str | None = None,
        nm_ids: list[int] | None = None,
        brand_names: list[str] | None = None,
        tag_ids: list[int] | None = None,
        skip_deleted_nm: bool = False,
    ) -> tuple[analytics.SalesFunnelProduct, ...] | None:
        """
        МЕТОД НЕ ДОДЕЛАН
        Метод формирует отчёт о товарах, сравнивая ключевые показатели за текущий период с аналогичным прошлым.
        Данные отчёта обновляются 1 раз в час.
        В течение часа после события появляется большая часть данных:
        о заказах
        о переходах в карточку товара
        о добавлениях товаров в корзину
        Малая часть этих данных может появляться в течение нескольких дней.
        Выкупы, отмены и возвраты отображаются в отчёте за тот день, когда товар был заказан. Например, если заказ был сделан 1 января, а покупатель вернул товар 10 января, данные об этом возврате появятся в отчёте за 1 января.
        Окончательные итоги продаж вы можете отслеживать с помощью детализаций к отчётам реализации.
        Параметры brandNames,subjectIds, tagIds, nmIds могут быть пустыми [], тогда в ответе возвращаются все карточки продавца.
        Если вы указали несколько параметров, в ответе будут карточки, в которых есть одновременно все эти параметры. Если карточки не подходят по параметрам запроса, вернётся пустой ответ [].
        Можно получить отчёт максимум за последние 365 дней.
        В данных предыдущего периода:
        Данные в pastPeriod указаны за такой же период, что и в selectedPeriod
        Если дата начала pastPeriod раньше, чем год назад от текущей даты, она будет приведена к виду: pastPeriod.start = текущая дата — 365 дней
        Можно использовать пагинацию.
        """
        ans = await self.get('/v3/sales-funnel/products', json={
            "selectedPeriod": {
                "start": "2023-06-01",
                "end": "2024-03-01"
            },
            "pastPeriod": {
                "start": "2023-06-01",
                "end": "2024-03-01"
            },
            "nmIds": [
                1234567
            ],
            "brandNames": [
                "nike",
                "adidas"
            ],
            "subjectIds": [
                64,
                334
            ],
            "tagIds": [
                32,
                53
            ],
            "skipDeletedNm": False,
            "orderBy": {
                "field": "openCard",
                "mode": "asc"
            },
            "limit": 231,
            "offset": 10
        })
        if ans.status == 200:
            return tuple(analytics.SalesFunnelProduct(**item) for item in ans.json['report'])
