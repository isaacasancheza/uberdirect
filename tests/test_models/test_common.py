import json

from pydantic import BaseModel

from uberdirect import fields


class Model(BaseModel):
    address: fields.StructuredAddress


def test_structured_address():
    address_data = dict(
        street_address=('Street 1',),
        city='CDMX',
        state='VZ',
        country='MX',
        zip_code='99999',
    )
    address_string = json.dumps(
        address_data,
        sort_keys=True,
        separators=(',', ':'),
    )

    model_1 = Model(address=address_data)  # type: ignore
    model_2 = Model.model_validate({'address': address_data})
    model_3 = Model.model_validate({'address': address_string})
    model_4 = Model.model_validate({'address': json.dumps(address_data)})

    assert model_1.address == model_2.address == model_3.address == model_4.address
    assert model_1.model_dump(mode='json')['address'] == address_string
