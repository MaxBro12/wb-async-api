from .base import WbBaseService

from .settings import Settings


class FinancesService(WbBaseService):
    def __init__(self, token: str):
        super().__init__(
            base_url=Settings.WB_FINANCES_URL,
            token=token,
        )
