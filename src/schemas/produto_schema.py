from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProdutoCreateRequest(BaseModel):
    nome: str = Field(...)
    sku_codigo: str = Field(...)
    precoCusto: float
    precoVenda: float
    qtdEmEstoque: int
    idCategoria: int
    idFornecedor: int
    
class ProdutoCreateSucess(BaseModel):
    message: str


class ProdutoReadSucess(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    sku_codigo: str
    precoCusto: float
    precoVenda: float
    qtdEmEstoque: int
    dataCadastro: datetime
    idCategoria: int
    idFornecedor: int