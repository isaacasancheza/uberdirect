from pydantic import BaseModel


class StructuredAddress(BaseModel):
    street_address: tuple[str] | tuple[str, str]
    district: str
    city: str
    state: str
    zip_code: str
    country: str

    @property
    def serialized(self) -> str:
        return self.model_dump_json(exclude_none=True)
