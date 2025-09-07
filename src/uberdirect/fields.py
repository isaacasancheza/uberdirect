from decimal import Decimal
from typing import Annotated, Any

from pydantic import BaseModel, GetCoreSchemaHandler, PlainSerializer
from pydantic_core import core_schema
from pydantic_extra_types.phone_numbers import PhoneNumberValidator


class DecimalFromInt(Decimal):
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
        )

    @classmethod
    def _int_to_decimal(cls, value: int) -> Decimal:
        return Decimal(str(value / 100))


class _StructuredAddressAnnotation(BaseModel):
    street_address: tuple[str] | tuple[str, str]
    city: str
    state: str
    zip_code: str
    country: str


def _serialize_structuerd_address(address: _StructuredAddressAnnotation) -> str:
    return address.model_dump_json()


type StructuredAddress = Annotated[
    _StructuredAddressAnnotation,
    PlainSerializer(
        func=_serialize_structuerd_address,
        when_used='json',
    ),
]

type PhoneNumber = Annotated[
    str,
    PhoneNumberValidator(
        number_format='E164',
        default_region='MX',
    ),
]
