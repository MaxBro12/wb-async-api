from typing import Tuple, List

from .base import WbBaseService
from .data_classes import marketplace

from .settings import Settings


class MarketplaceService(WbBaseService):
    def __init__(self, token: str, test: bool = False):
        super().__init__(
            base_url=Settings.WB_MARKET_TEST_URL if test else Settings.WB_MARKET_URL,
            token=token,
        )

    async def offices(self) -> Tuple[marketplace.Office, ...] | None:
        """
        Получает список офисов.
        """
        ans = await self.get('/api/v3/offices')
        if ans.status == 200:
            return tuple(marketplace.Office(**item) for item in ans.json)

    async def warehouses(self) -> Tuple[marketplace.Warehouse, ...] | None:
        """
        Получает список складов.
        """
        ans = await self.get('/api/v3/warehouses')
        if ans.status == 200:
            return tuple(marketplace.Warehouse(**item) for item in ans.json)

    async def warehouse_contracts(
        self, warehouse_id: int
    ) -> Tuple[marketplace.WarehouseContract, ...] | None:
        """
        Получает список контактов склада.
        """
        ans = await self.get(f'v3/dbw/warehouses/{warehouse_id}/contacts')
        if ans.status == 200:
            return tuple(marketplace.WarehouseContract(**item) for item in ans.json['contacts'])

    async def warehouse_stocks(
        self, warehouse_id: int,
        chrtIds: List[int] | Tuple[int, ...] | None
    ) -> Tuple[marketplace.WarehouseStock, ...] | None:
        """
        Получает список остатков товаров на складе.
        СКОРЕЕ ВСЕГО НЕ РАБОТАЕТ НАДО ТЕСТИРОВАТЬ
        """
        ans = await self.post(f'v3/dbw/warehouses/{warehouse_id}/stocks', json={
            'chrtIds': chrtIds
        })
        if ans.status == 200:
            return tuple(marketplace.WarehouseStock(**item) for item in ans.json['stocks'])
