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
        request: models.QuoteRequest,
    ) -> models.QuoteResponse:
        """
        Create quote.

        https://developer.uber.com/docs/deliveries/api-reference/daas#tag/Quotes/paths/~1customers~1%7Bcustomer_id%7D~1delivery_quotes/post
        """
        body = request.model_dump(
            exclude_none=True,
        )
        response = self._post(
            body,
            'delivery_quotes',
        )
        return models.QuoteResponse.model_validate(response)
