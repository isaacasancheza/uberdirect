from uberdirect import models
from uberdirect.core.base import Base


class Deliveries(Base):
    """
    Deliveries

    https://developer.uber.com/docs/deliveries/api-reference/daas#tag/Delivery
    """

    def create_delivery(
        self,
        *,
        request: models.DeliveryCreateRequest,
    ) -> models.Delivery:
        body = request.model_dump(
            exclude_none=True,
        )
        response = self._post(body, 'deliveries')
        return models.Delivery.model_validate(response)

    def update_delivery(
        self,
        /,
        delivery_id: str,
        *,
        request: models.DeliveryUpdateRequest,
    ) -> models.Delivery:
        body = request.model_dump(
            exclude_none=True,
        )
        response = self._post(body, 'deliveries', delivery_id)
        return models.Delivery.model_validate(response)

    def cancel_delivery(
        self,
        /,
        delivery_id: str,
    ) -> models.Delivery:
        response = self._post({}, 'deliveries', delivery_id, 'cancel')
        return models.Delivery.model_validate(response)
