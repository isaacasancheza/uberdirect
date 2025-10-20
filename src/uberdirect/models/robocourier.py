from datetime import datetime
from typing import Literal

from uberdirect import constants
from uberdirect.models.base import BaseModel


class RoboCourier(BaseModel):
    mode: constants.RoboCourierMode
    cancel_reason: constants.RoboCourierCancelReason | None = None


class RoboCourierAuto(RoboCourier):
    """
    https://developer.uber.com/docs/deliveries/guides/robocourier
    """

    mode: Literal[constants.RoboCourierMode.AUTO]


class RoboCourierCustom(RoboCourier):
    """
    https://developer.uber.com/docs/deliveries/guides/robocourier
    """

    mode: Literal[constants.RoboCourierMode.CUSTOM]
    enroute_for_pickup_at: datetime

    pickup_at: datetime
    pickup_imminent_at: datetime

    dropoff_at: datetime
    dropoff_imminent_at: datetime
