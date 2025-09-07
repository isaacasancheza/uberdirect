from decimal import Decimal
from typing import Annotated, Any

from pydantic import GetCoreSchemaHandler
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


type PhoneNumber = Annotated[
    str,
    PhoneNumberValidator(
        number_format='E164',
        default_region='MX',
    ),
]
