from .base import WbBaseService

from .settings import Settings


class CommonService(WbBaseService):
    def __init__(self, token: str):
        super().__init__(
            base_url=Settings.WB_COMMON_URL,
            token=token,
        )
