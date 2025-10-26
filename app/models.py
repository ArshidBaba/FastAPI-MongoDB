from pydantic import BaseModel, Field

class Item(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    name: str
    description: str | None = None
    price: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True