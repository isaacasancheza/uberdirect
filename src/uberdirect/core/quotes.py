from uberdirect import models
from uberdirect.core.base import Base


class Quotes(Base):
    """
    Quotes

    https://developer.uber.com/docs/deliveries/api-reference/daas#tag/Quotes
    """

    def create_quote(
        self,
        *,
        request: models.QuoteCreateRequest,
    ) -> models.QuoteCreateResponse:
        response = self._post(
            request,
            'delivery_quotes',
        )
        return models.QuoteCreateResponse.model_validate(response)
