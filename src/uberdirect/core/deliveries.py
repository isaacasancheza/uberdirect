from uberdirect import uberdirect_models
from uberdirect.core.base import Base


class Deliveries(Base):
    """
    Deliveries

    https://developer.uber.com/docs/deliveries/api-reference/daas#tag/Delivery
    """

    def create_delivery(
        self,
        *,
        request: uberdirect_models.DeliveryRequest,
    ) -> uberdirect_models.DeliveryResponse:
        body = request.model_dump(
            exclude_none=True,
        )
        response = self._post(body, 'deliveries')
        return uberdirect_models.DeliveryResponse.model_validate(response)
