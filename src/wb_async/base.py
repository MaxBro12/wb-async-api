from core.requests_makers import HttpMakerAsync, ResponseData
from .exceptions import (
    NotAuthorized,
    TooManyRequests,
    AccessDenied,
    PaymentRequired,
    IncorrectRequest,
)


class WbBaseService(HttpMakerAsync):
    def __init__(self, base_url: str, token: str):
        super().__init__(
            base_url=base_url,
            base_headers={
                'Authorization': token
            },
            parse_method=WbBaseService._handle_response
        )

    @classmethod
    async def _handle_response(cls, response) -> ResponseData:
        match response.status:
            case 400:
                raise IncorrectRequest(response.status, (await response.json()).get('detail', 'Adt data not available'))
            case 401:
                raise NotAuthorized((await response.json()).get('detail', 'Adt data not available'))
            case 402:
                raise PaymentRequired((await response.json()).get('detail', 'Adt data not available'))
            case 403:
                raise AccessDenied((await response.json()).get('data', 'Adt data not available'))
            case 429:
                raise TooManyRequests((await response.json()).get('detail', 'Adt data not available'))
        return await super()._get_simple_response(response)
