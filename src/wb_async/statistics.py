from typing import Literal

from core.requests_makers.asyncio_limiter import WindowRateLimiter
from .base import WbBaseService
from .data_classes import statistics, globals

from .settings import Settings


class StatisticsService(WbBaseService):
    def __init__(self, token: str, test: bool = False):
        super().__init__(
            base_url=Settings.WB_STATISTICS_TEST_URL if test else Settings.WB_STATISTICS_URL,
            token=token,
        )

    @WindowRateLimiter(max_calls=1, time_window=65)
    async def daily_reports(self,
        date_from: str,
        date_to: str,
        limit: int = 1000,
        rrdid: int | None = None,
        period: Literal['daily', 'weekly'] = 'weekly',
    ) -> tuple[globals.ResponseData, ...] | None:
        params = {
            'dateFrom': date_from,
            'dateTo': date_to,
            'limit': min(limit, 100_000), # есть ограничение на максимальное количество
            'period': period,
        }
        if rrdid is not None:
            params['rrdid'] = rrdid
        ans = await self.get('/v5/supplier/reportDetailByPeriod', params=params)
        if ans.status == 200:
            return ans.json
        elif ans.status == 204:
            return tuple()

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def balance(self) -> statistics.Balance | None:
        ans = await self.get('/v1/account/balance')
        if ans.status == 200:
            return statistics.Balance(**ans.json)

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def supplier_stocks(
        self,
        date_from: str
    ) -> tuple[statistics.SupplierStockItem, ...] | None:
        ans = await self.get('/v1/supplier/stocks', params={'dateFrom': date_from})
        if ans.status == 200:
            return tuple([statistics.SupplierStockItem(**item) for item in ans.json])
        return None

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def supplier_orders(
        self,
        date_from: str,
        flag: int = 0
    ) -> tuple[statistics.SupplierOrderItem, ...] | None:
        ans = await self.get('/v1/supplier/orders', params={'dateFrom': date_from, 'flag': flag})
        if ans.status == 200:
            return tuple([statistics.SupplierOrderItem(**item) for item in ans.json])
        return None

    @WindowRateLimiter(max_calls=1, time_window=60)
    async def supplier_sales(
        self,
        date_from: str
    ) -> tuple[statistics.SupplierSalesItem, ...] | None:
        ans = await self.get('/v1/supplier/sales', params={'dateFrom': date_from})
        if ans.status == 200:
            return tuple([statistics.SupplierSalesItem(**item) for item in ans.json])
        return None
