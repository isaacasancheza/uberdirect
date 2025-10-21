from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from uberdirect import constants
from uberdirect.models.base import BaseModel

type RoboCourier = Annotated[
    RoboCourierAuto | RoboCourierCustom,
    Field(
        discriminator='mode',
    ),
]


class RoboCourierAuto(BaseModel):
    """
    https://developer.uber.com/docs/deliveries/guides/robocourier
    """

    mode: Literal[constants.RoboCourierMode.AUTO]
    cancel_reason: constants.RoboCourierCancelReason | None = None


class RoboCourierCustom(BaseModel):
    """
    https://developer.uber.com/docs/deliveries/guides/robocourier
    """

    mode: Literal[constants.RoboCourierMode.CUSTOM]
    enroute_for_pickup_at: datetime

    pickup_at: datetime
    pickup_imminent_at: datetime

    dropoff_at: datetime
    dropoff_imminent_at: datetime
