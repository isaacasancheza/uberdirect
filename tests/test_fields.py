from decimal import Decimal

from pydantic import BaseModel

from uberpy import fields


class Model(BaseModel):
    number: fields.DecimalFromInt


def test_decimal_from_int():
    number = Decimal('99.99')
    number_int = int(number * 100)

    model_1 = Model(number=number)
    model_2 = Model.model_validate({'number': number_int})
    model_3 = Model.model_validate({'number': number})

    assert model_1.number == model_2.number == model_3.number
    assert model_1.number == number
    assert model_1.model_dump(mode='json')['number'] == number_int
    assert model_2.number == number
    assert model_3.number == number

    assert all(
        isinstance(model.number, Decimal) for model in [model_1, model_2, model_3]
    )
