from __future__ import annotations

import json
from decimal import Decimal
from typing import Annotated, Any, ClassVar, TypedDict

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_extra_types.phone_numbers import PhoneNumberValidator


class Latitude(Decimal):
    min: ClassVar[Decimal] = Decimal(-90.00)
    max: ClassVar[Decimal] = Decimal(90.00)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.decimal_schema(ge=Decimal(cls.min), le=Decimal(cls.max))


class Longitude(Decimal):
    min: ClassVar[Decimal] = Decimal(-180.00)
    max: ClassVar[Decimal] = Decimal(180.00)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.decimal_schema(ge=Decimal(cls.min), le=Decimal(cls.max))


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


type PhoneNumber = Annotated[
    str,
    PhoneNumberValidator(
        number_format='E164',
        default_region='MX',
    ),
]
type DecimalFromInt = Annotated[Decimal, _DecimalFromIntAnnotation]
type StructuredAddress = Annotated[_StructuredAddressDict, _StructuredAddressAnnotation]
