from .advert import AdvertService
from .analytics import AnalyticsService
from .common import CommonService
from .content import ContentService
from .feedback import FeedbackService
from .finances import FinancesService
from .marketplace import MarketplaceService
from .statistics import StatisticsService


class WBService:
    advert: AdvertService
    analytics: AnalyticsService
    common: CommonService
    content: ContentService
    feedback: FeedbackService
    finances: FinancesService
    marketplace: MarketplaceService
    statistics: StatisticsService

    def __init__(self, token: str, test: bool = False):
        self.advert = AdvertService(token=token, test=test)
        self.analytics = AnalyticsService(token=token)
        self.common = CommonService(token=token)
        self.content = ContentService(token=token, test=test)
        self.feedback = FeedbackService(token=token)
        self.finances = FinancesService(token=token)
        self.marketplace = MarketplaceService(token=token, test=test)
        self.statistics = StatisticsService(token=token, test=test)
