from pydantic import Field, BaseModel


class PessoaRequest(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=500)
    price: float = Field(gt=0)
    is_available: bool
