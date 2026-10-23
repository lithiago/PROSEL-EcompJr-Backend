from pydantic import BaseModel, ConfigDict, Field


class FornecedorCreateRequest(BaseModel):
    nome: str = Field(..., min_length=1)


class FornecedorUpdateRequest(BaseModel):
    nome: str = Field(..., min_length=1)


class FornecedorCreateSucess(BaseModel):
    message: str


class FornecedorReadSucess(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str