from datetime import datetime, timezone

from pydantic import BaseModel

from uberpy import constants, models


class Model(BaseModel):
    robocourier: models.RoboCourier


def test_robocourier():
    now = datetime.now(timezone.utc)

    Model(
        robocourier=models.RoboCourierAuto(
            mode=constants.RoboCourierMode.AUTO,
        )
    )

    Model(
        robocourier=models.RoboCourierCustom(
            mode=constants.RoboCourierMode.CUSTOM,
            enroute_for_pickup_at=now,
            pickup_at=now,
            pickup_imminent_at=now,
            dropoff_at=now,
            dropoff_imminent_at=now,
        )
    )
