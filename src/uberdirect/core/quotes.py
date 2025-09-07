from uberdirect import uberdirect_models
from uberdirect.core.base import Base


class Quotes(Base):
    """
    Quotes

    https://developer.uber.com/docs/deliveries/api-reference/daas#tag/Quotes
    """

    def create_quote(
        self,
        *,
        request: uberdirect_models.QuoteRequest,
    ) -> uberdirect_models.QuoteResponse:
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
        return uberdirect_models.QuoteResponse.model_validate(response)
