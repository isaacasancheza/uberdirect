import requests

from uberdirect.core.base import AccessToken, APIVersion, Base
from uberdirect.core.deliveries import Deliveries
from uberdirect.core.quotes import Quotes


class UberDirect(Base):
    def __init__(
        self,
        customer_id: str,
        access_token: AccessToken,
        /,
        *,
        version: APIVersion,
        timeout: float | None = None,
        session: requests.Session | None = None,
        jitter_max: float | None = None,
        max_retries: int | None = None,
        retriable_http_codes: set[int] | None = None,
    ) -> None:
        session = session or requests.Session()
        super().__init__(
            customer_id,
            access_token,
            version=version,
            timeout=timeout,
            session=session,
            jitter_max=jitter_max,
            max_retries=max_retries,
            retriable_http_codes=retriable_http_codes,
        )
        self.quotes = Quotes(
            customer_id,
            access_token,
            version=version,
            timeout=timeout,
            session=session,
            jitter_max=jitter_max,
            max_retries=max_retries,
            retriable_http_codes=retriable_http_codes,
        )
        self.deliveries = Deliveries(
            customer_id,
            access_token,
            version=version,
            timeout=timeout,
            session=session,
            jitter_max=jitter_max,
            max_retries=max_retries,
            retriable_http_codes=retriable_http_codes,
        )
