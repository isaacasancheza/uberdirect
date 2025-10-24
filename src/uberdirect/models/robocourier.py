from typing import Annotated, Literal

from pydantic import AwareDatetime, Field

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

    enroute_for_pickup_at: AwareDatetime
    """
    If a pickup window is specified, it must occur within the pickup window. Else, must occur within 30 minutes of the order being placed
    """

    pickup_at: AwareDatetime
    pickup_imminent_at: AwareDatetime

    dropoff_at: AwareDatetime
    """
    Must be within 8 hours of pickup time
    """

    dropoff_imminent_at: AwareDatetime
