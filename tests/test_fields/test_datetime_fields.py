from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, ValidationError
from pytest import raises

from uberdirect import fields


class Model(BaseModel):
    pickup_ready_dt: datetime | None = None
    pickup_deadline_dt: fields.PickupDeadlineDt | None = None
    dropoff_ready_dt: fields.DropoffReadyDt | None = None
    dropoff_deadline_dt: fields.DropoffDeadlineDt | None = None


def test_datetime_fields():
    now = datetime.now(timezone.utc)

    # empty fields
    Model()

    # some non empty fields
    Model(
        pickup_ready_dt=now,
        dropoff_deadline_dt=now,
    )

    # pickup_deadline_dt must be at least 10 mins later than pickup_ready_dt
    pickup_ready_dt = now
    pickup_deadline_dt = now + timedelta(minutes=9)
    with raises(ValidationError) as e:
        Model(
            pickup_ready_dt=pickup_ready_dt,
            pickup_deadline_dt=pickup_deadline_dt,
        )
    assert e.value.error_count() == 1
    assert e.value.errors()[0]['type'] == 'pickup_ready_dt'

    # dropoff_ready_dt must be less than or equal to pickup_deadline_dt
    pickup_ready_dt = now
    pickup_deadline_dt = pickup_ready_dt + timedelta(minutes=10)
    dropoff_ready_dt = pickup_deadline_dt + timedelta(seconds=1)
    with raises(ValidationError) as e:
        Model(
            pickup_ready_dt=pickup_ready_dt,
            pickup_deadline_dt=pickup_deadline_dt,
            dropoff_ready_dt=dropoff_ready_dt,
        )
    assert e.value.error_count() == 1
    assert e.value.errors()[0]['type'] == 'pickup_deadline_dt'

    # dropoff_deadline_dt must be at least 20 mins later than dropoff_ready_dt
    pickup_ready_dt = now
    pickup_deadline_dt = pickup_ready_dt + timedelta(minutes=10)
    dropoff_ready_dt = pickup_ready_dt
    dropoff_deadline_dt = dropoff_ready_dt - timedelta(minutes=19)
    with raises(ValidationError) as e:
        Model(
            pickup_ready_dt=pickup_ready_dt,
            pickup_deadline_dt=pickup_deadline_dt,
            dropoff_ready_dt=dropoff_ready_dt,
            dropoff_deadline_dt=dropoff_deadline_dt,
        )
    assert e.value.error_count() == 1
    assert e.value.errors()[0]['type'] == 'dropoff_ready_dt'

    # dropoff_deadline_dt must be greater than or equal to pickup_deadline_dt
    pickup_ready_dt = now
    pickup_deadline_dt = pickup_ready_dt + timedelta(minutes=60)
    dropoff_ready_dt = pickup_ready_dt
    dropoff_deadline_dt = dropoff_ready_dt + timedelta(minutes=20)
    with raises(ValidationError) as e:
        Model(
            pickup_ready_dt=pickup_ready_dt,
            pickup_deadline_dt=pickup_deadline_dt,
            dropoff_ready_dt=dropoff_ready_dt,
            dropoff_deadline_dt=dropoff_deadline_dt,
        )
    assert e.value.error_count() == 1
    assert e.value.errors()[0]['type'] == 'pickup_deadline_dt'

    # ok
    pickup_ready_dt = now
    pickup_deadline_dt = pickup_ready_dt + timedelta(minutes=10)
    dropoff_ready_dt = pickup_ready_dt
    dropoff_deadline_dt = dropoff_ready_dt + timedelta(minutes=20)
    Model(
        pickup_ready_dt=pickup_ready_dt,
        pickup_deadline_dt=pickup_deadline_dt,
        dropoff_ready_dt=dropoff_ready_dt,
        dropoff_deadline_dt=dropoff_deadline_dt,
    )
