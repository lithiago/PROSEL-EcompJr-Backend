from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from .base import Base

class Produto(Base):
    __tablename__ = "Produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)

    sku_codigo = Column(Integer, nullable=False, index=True)

    precoCusto = Column(Float, nullable=False)
    precoVenda = Column(Float, nullable=False)

    qtdEmEstoque = Column(Integer, nullable=False)

    dataCadastro = Column(DateTime, nullable=False)

    idCategoria = Column(
        Integer,
        ForeignKey("Categoria.id"),
        nullable=False,
        index=True
    )

    idFornecedor = Column(
        Integer,
        ForeignKey("Fornecedor.id"),
        nullable=False,
        index=True
    )