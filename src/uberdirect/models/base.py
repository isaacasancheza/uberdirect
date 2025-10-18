from pydantic import BaseModel as PydanticBaseModel
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    model_config = {
        'extra': 'ignore',
        'alias_generator': to_camel,
        'use_enum_values': True,
        'from_attributes': True,
        'validate_by_name': True,
        'validate_by_alias': True,
    }
