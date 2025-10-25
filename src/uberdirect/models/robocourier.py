from datetime import datetime, timedelta
from typing import Annotated, Literal

from pydantic import AwareDatetime, Field, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

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
    """
    Fixed value.
    """

    cancel_reason: constants.RoboCourierCancelReason | None = None
    """
    Cancel reason.
    """


class RoboCourierCustom(BaseModel):
    """
    https://developer.uber.com/docs/deliveries/guides/robocourier
    """

    mode: Literal[constants.RoboCourierMode.CUSTOM]
    """
    Fixed value.
    """

    enroute_for_pickup_at: AwareDatetime
    """
    If a pickup window is specified, it must occur within the pickup window. 
    Else, must occur within 30 minutes of the order being placed.
    """

    pickup_at: AwareDatetime
    """
    Must be greater than equal to enroute_for_pickup_at.
    """

    pickup_imminent_at: AwareDatetime
    """
    Must be less than equal to pickup_at.
    """

    dropoff_at: AwareDatetime
    """
    Must be within 8 hours of pickup time.
    """

    dropoff_imminent_at: AwareDatetime
    """
    Must be less than equal to dropoff_at.
    """

    @field_validator('pickup_at')
    @classmethod
    def validate_pickup_at(
        cls,
        pickup_at: datetime,
        info: ValidationInfo,
    ) -> datetime:
        """
        pickup_at must be greater than equal to enroute_for_pickup_at
        """
        enroute_for_pickup_at: datetime = info.data['enroute_for_pickup_at']
        if pickup_at < enroute_for_pickup_at:
            raise PydanticCustomError(
                'enroute_for_pickup_at',
                'pickup_at must be greater than equal to enroute_for_pickup_at',
            )
        return pickup_at

    @field_validator('pickup_imminent_at')
    @classmethod
    def validate_pickup_imminent_at(
        cls,
        pickup_imminent_at: datetime,
        info: ValidationInfo,
    ) -> datetime:
        """
        pickup_imminent_at must be less than equal to pickup_at
        """
        pickup_at: datetime = info.data['pickup_at']
        if pickup_imminent_at > pickup_at:
            raise PydanticCustomError(
                'pickup_at',
                'pickup_imminent_at must be less than equal to pickup_at',
            )
        return pickup_imminent_at

    @field_validator('dropoff_at')
    @classmethod
    def validate_dropoff_at(
        cls,
        dropoff_at: datetime,
        info: ValidationInfo,
    ) -> datetime:
        """
        dropoff_at must be less than equal to pickup_at + timedelta(hours=8)
        """
        pickup_at: datetime = info.data['pickup_at']
        deadline = pickup_at + timedelta(hours=8)
        if dropoff_at > deadline:
            raise PydanticCustomError(
                'pickup_at',
                'dropoff_at must be less than equal to pickup_at + timedelta(hours=8)',
            )
        return dropoff_at

    @field_validator('dropoff_imminent_at')
    @classmethod
    def validate_dropoff_imminent_at(
        cls,
        dropoff_imminent_at: datetime,
        info: ValidationInfo,
    ) -> datetime:
        """
        dropoff_imminent_at must be less than equal to dropoff_at
        """
        dropoff_at: datetime = info.data['dropoff_at']
        if dropoff_imminent_at > dropoff_at:
            raise PydanticCustomError(
                'dropoff_at',
                'dropoff_imminent_at must be less than equal to dropoff_at',
            )
        return dropoff_imminent_at
