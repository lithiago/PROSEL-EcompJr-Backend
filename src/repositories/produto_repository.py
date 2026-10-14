
from datetime import datetime

from sqlalchemy.orm import Session

from src.models.produto import Produto


def buscar_por_sku_codigo(db: Session, sku_codigo: str):
    return db.query(Produto).filter(Produto.sku_codigo == sku_codigo).first()


def listar_produtos(db: Session) -> list[Produto]:
    return db.query(Produto).all()


def criar_produto(
    db: Session,
    nome: str,
    sku_codigo: str,
    precoCusto: float,
    precoVenda: float,
    qtdEstoque: int,
    dataCadastro: datetime,
    idCategoria: int,
    idFornecedor: int,
):
    produto = Produto(
        nome=nome,
        sku_codigo=sku_codigo,
        precoCusto=precoCusto,
        precoVenda=precoVenda,
        qtdEmEstoque=qtdEstoque,
        dataCadastro=dataCadastro,
        idCategoria=idCategoria,
        idFornecedor=idFornecedor,
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto