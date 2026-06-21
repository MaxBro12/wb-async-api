from typing import List, Tuple, Literal

from .base import WbBaseService
from .data_classes import advert

from .settings import Settings


class AdvertService(WbBaseService):
    def __init__(self, token: str, test: bool = False):
        super().__init__(
            base_url=Settings.WB_ADVERT_TEST_URL if test else Settings.WB_ADVERT_URL,
            token=token,
        )

    async def companies(self) -> advert.Adverts | None:
        ans = await self.get('/v1/promotion/count')
        if ans.status == 200:
            return advert.Adverts(**ans.json)

    async def companies_info(
        self,
        ids: List[int] | Tuple[int],
        statuses: List[int] | Tuple[int],
        payment_type: Literal['cpm', 'cpc']
    ) -> advert.CompanyInfo | None:
        if len(ids) > 50:
            return None # Должно вызывать исключение
        ans = await self.get('/v2/adverts', params={
            'ids': ','.join(map(str, ids)),
            'statuses': ','.join(map(str, statuses)),
            'payment_type': payment_type
        })
        if ans.status == 200:
            return advert.CompanyInfo(**ans.json)

    async def balance(self) -> advert.Balance | None:
        ans = await self.get('/v1/balance')
        if ans.status == 200:
            return advert.Balance(**ans.json)

    async def company_cache(self, company_id: int) -> advert.CompanyCache | None:
        ans = await self.get(f'/v1/company/{company_id}')
        if ans.status == 200:
            return advert.CompanyCache(**ans.json)

    async def cost_history(self, date_from: str, date_to: str) -> advert.CostHistory | None:
        ans = await self.get('/v1/cost/history', params={
            'from': date_from,
            'to': date_to
        })
        if ans.status == 200:
            return advert.CostHistory(**ans.json)

    async def payments(self) -> advert.Payments | None:
        ans = await self.get('/v1/payments')
        if ans.status == 200:
            return advert.Payments(**ans.json)
