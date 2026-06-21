from typing import Literal

from .base import WbBaseService
from .data_classes.globals import Locale
from .data_classes.content import ParentProductCategories, ProductsList, CharacteristicsList


from .settings import Settings


class ContentService(WbBaseService):
    def __init__(self, token: str, test: bool = False):
        super().__init__(
            base_url=Settings.WB_CONTENT_TEST_URL if test else Settings.WB_CONTENT_URL,
            token=token,
        )

    async def parent_objects_categories(self) -> ParentProductCategories | None:
        ans = await self.get('/v2/object/parent/all')
        if ans.status == 200:
            return ParentProductCategories(**ans.json)
        return None

    async def objects_list(self,
        locale: Locale = 'en',
        name: str | None = None,
        limit: int = 30,
        offset: int = 0,
        parentID: int | None = None,
    ) -> ProductsList | None:
        params = {
            'locale': locale,
            'limit': limit,
            'offset': offset,
        }
        if name:
            params['name'] = name
        if parentID:
            params['parentID'] = parentID
        ans = await self.get('v2/object/all', params=params)
        if ans.status == 200:
            return ProductsList(**ans.json)
        return None

    async def characteristics_of_objects(
        self,
        subject_id: int,
        locale: Locale = 'en'
    ) -> CharacteristicsList | None:
        ans = await self.get(f'/v2/object/charcs/{subject_id}', params={'locale': locale})
        if ans.status == 200:
            return CharacteristicsList(**ans.json)
        return None
