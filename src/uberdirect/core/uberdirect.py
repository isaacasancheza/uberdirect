from uberdirect.core.base import AccessToken, APIVersion
from uberdirect.core.deliveries import Deliveries
from uberdirect.core.quotes import Quotes


class UberDirect:
    def __init__(
        self,
        customer_id: str,
        access_token: AccessToken,
        /,
        *,
        version: APIVersion,
        max_retries: int | None = None,
        retriable_http_codes: set[int] | None = None,
    ) -> None:
        self.quotes = Quotes(
            customer_id,
            access_token,
            version=version,
            max_retries=max_retries,
            retriable_http_codes=retriable_http_codes,
        )
        self.deliveries = Deliveries(
            customer_id,
            access_token,
            version=version,
            max_retries=max_retries,
            retriable_http_codes=retriable_http_codes,
        )
