import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Annotated, Any, TypedDict

from pydantic import AfterValidator, AwareDatetime, GetCoreSchemaHandler, ValidationInfo
from pydantic_core import PydanticCustomError, core_schema
from pydantic_extra_types.phone_numbers import PhoneNumberValidator


class _StructuredAddressDict(TypedDict):
    street_address: tuple[str] | tuple[str, str]
    city: str
    state: str
    zip_code: str
    country: str


class _StructuredAddressAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        schema = handler.generate_schema(source_type)
        return core_schema.union_schema(
            [
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(cls._parse_str),
                        schema,
                    ],
                ),
                schema,
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize
            ),
        )

    @classmethod
    def _parse_str(cls, value: str) -> _StructuredAddressDict:
        return _StructuredAddressDict(json.loads(value))

    @classmethod
    def _serialize(cls, value: _StructuredAddressDict | str) -> str:
        if isinstance(value, str):
            return value
        return json.dumps(
            value,
            sort_keys=True,
            separators=(',', ':'),
        )


class _DecimalFromIntAnnotation(Decimal):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.union_schema(
            [
                core_schema.chain_schema(
                    [
                        core_schema.int_schema(),
                        core_schema.no_info_plain_validator_function(
                            cls._int_to_decimal,
                        ),
                    ]
                ),
                core_schema.decimal_schema(decimal_places=2),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._decimal_to_int
            ),
        )

    @classmethod
    def _int_to_decimal(cls, value: int) -> Decimal:
        return Decimal(str(value / 100))

    @classmethod
    def _decimal_to_int(cls, value: int | Decimal) -> int:
        if isinstance(value, Decimal):
            return int(value * 100)
        return value


def _validate_pickup_deadline_dt(
    pickup_deadline_dt: datetime | None,
    info: ValidationInfo,
) -> datetime | None:
    """
    pickup_deadline_dt must be at least 10 mins later than pickup_ready_dt
    """
    pickup_ready_dt: datetime | None = info.data.get('pickup_ready_dt')
    if pickup_ready_dt and pickup_deadline_dt:
        window = pickup_deadline_dt - pickup_ready_dt
        if window < timedelta(minutes=10):
            raise PydanticCustomError(
                'pickup_ready_dt',
                'must be at least 10 mins later than pickup_ready_dt',
            )
    return pickup_deadline_dt


def _validate_dropoff_ready_dt(
    dropoff_ready_dt: datetime | None,
    info: ValidationInfo,
) -> datetime | None:
    """
    dropoff_ready_dt must be less than or equal to pickup_deadline_dt
    """
    pickup_deadline_dt: datetime | None = info.data.get('pickup_deadline_dt')
    if dropoff_ready_dt and pickup_deadline_dt:
        if dropoff_ready_dt > pickup_deadline_dt:
            raise PydanticCustomError(
                'pickup_deadline_dt',
                'must be less than or equal to pickup_deadline_dt',
            )
    return dropoff_ready_dt


def _validate_dropoff_deadline_dt(
    dropoff_deadline_dt: datetime | None,
    info: ValidationInfo,
) -> datetime | None:
    """
    dropoff_deadline_dt must be at least 20 mins later than dropoff_ready_dt and must be greater than or equal to pickup_deadline_dt.
    """
    dropoff_ready_dt: datetime | None = info.data.get('dropoff_ready_dt')
    pickup_deadline_dt: datetime | None = info.data.get('pickup_deadline_dt')
    if dropoff_ready_dt and pickup_deadline_dt and dropoff_deadline_dt:
        # dropoff_deadline_dt must be at least 20 mins later than dropoff_ready_dt
        window = dropoff_deadline_dt - dropoff_ready_dt
        if window < timedelta(minutes=20):
            raise PydanticCustomError(
                'dropoff_ready_dt',
                'must be at least 20 mins later than dropoff_ready_dt',
            )
        # dropoff_deadline_dt must be greater than or equal to pickup_deadline_dt
        if dropoff_deadline_dt < pickup_deadline_dt:
            raise PydanticCustomError(
                'pickup_deadline_dt',
                'must be greater than or equal to pickup_deadline_dt',
            )
    return dropoff_deadline_dt


type PhoneNumber = Annotated[
    str,
    PhoneNumberValidator(
        number_format='E164',
        default_region='MX',
    ),
]

type DecimalFromInt = Annotated[
    Decimal,
    _DecimalFromIntAnnotation,
]

type StructuredAddress = Annotated[
    _StructuredAddressDict,
    _StructuredAddressAnnotation,
]

type PickupDeadlineDt = Annotated[
    AwareDatetime,
    AfterValidator(
        _validate_pickup_deadline_dt,
    ),
]

type DropoffReadyDt = Annotated[
    AwareDatetime,
    AfterValidator(
        _validate_dropoff_ready_dt,
    ),
]

type DropoffDeadlineDt = Annotated[
    AwareDatetime,
    AfterValidator(
        _validate_dropoff_deadline_dt,
    ),
]
