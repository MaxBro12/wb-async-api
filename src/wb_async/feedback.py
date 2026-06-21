from .base import WbBaseService

from .settings import Settings


class FeedbackService(WbBaseService):
    def __init__(self, token: str):
        super().__init__(
            base_url=Settings.WB_FEEDBACK_URL,
            token=token,
        )
