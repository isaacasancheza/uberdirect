from datetime import datetime, timezone

from pydantic import BaseModel

from uberdirect import constants, models


class Model(BaseModel):
    robo_courier: models.RoboCourier


def test_robo_courier():
    now = datetime.now(timezone.utc)

    Model(
        robo_courier=models.RoboCourierAuto(
            mode=constants.RoboCourierMode.AUTO,
        )
    )

    Model(
        robo_courier=models.RoboCourierCustom(
            mode=constants.RoboCourierMode.CUSTOM,
            enroute_for_pickup_at=now,
            pickup_at=now,
            pickup_imminent_at=now,
            dropoff_at=now,
            dropoff_imminent_at=now,
        )
    )
