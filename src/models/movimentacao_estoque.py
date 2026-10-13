from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from .base import Base

class TipoMovimentacao(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MovimentacaoEstoque(Base):
    __tablename__ = "MovimentacaoEstoque"

    id = Column(Integer, primary_key=True, index=True)

    tipo = Column(
        SQLEnum(TipoMovimentacao),
        nullable=False,
        index=True
    )

    quantidade = Column(
        Integer,
        nullable=False,
        index=True
    )

    data = Column(
        DateTime,
        nullable=False,
        index=True
    )

    idProduto = Column(
        Integer,
        ForeignKey("Produto.id"),
        nullable=False,
        index=True
    )