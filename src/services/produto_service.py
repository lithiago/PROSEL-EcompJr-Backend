
from datetime import datetime

from sqlalchemy.orm import Session

from src.errors.errors import ProdutoError
from src.repositories.produto_repository import (
    buscar_por_sku_codigo,
    buscar_produtos_por_categorias,
    buscar_produtos_por_fornecedores,
    criar_produto,
    listar_produtos_com_estoque_baixo,
    listar_produtos,
)
from src.schemas.produto_schema import ProdutoCreateSucess, ProdutoReadSucess


def criar_produto_service(
    db: Session,
    nome: str,
    sku_codigo: str,
    precoCusto: float,
    precoVenda: float,
    qtdEstoque: int,
    idCategoria: int,
    idFornecedor: int,
) -> ProdutoCreateSucess:
    produto = buscar_por_sku_codigo(db, sku_codigo)

    if produto:
        raise ProdutoError(
            "SKU_CODIGO_IN_USE",
            "O sku_codigo já está associado a um produto.",
            {"field": "sku_codigo", "rule": "sku_codigo_in_use"},
        )

    dataCadastro = datetime.now()

    criar_produto(
        db=db,
        nome=nome,
        sku_codigo=sku_codigo,
        precoCusto=precoCusto,
        precoVenda=precoVenda,
        qtdEstoque=qtdEstoque,
        dataCadastro=dataCadastro,
        idCategoria=idCategoria,
        idFornecedor=idFornecedor,
    )
    return ProdutoCreateSucess(message="Produto criado com sucesso.")


def get_produtos_service(db: Session) -> list[ProdutoReadSucess]:
    return [
        ProdutoReadSucess.model_validate(produto)
        for produto in listar_produtos(db)
    ]


def get_produtos_por_categoria_service(
    db: Session,
    categoria_id: int,
) -> list[ProdutoReadSucess]:
    return [
        ProdutoReadSucess.model_validate(produto)
        for produto in buscar_produtos_por_categorias(db, [categoria_id])
    ]


def get_produtos_por_fornecedor_service(
    db: Session,
    fornecedor_id: int,
) -> list[ProdutoReadSucess]:
    return [
        ProdutoReadSucess.model_validate(produto)
        for produto in buscar_produtos_por_fornecedores(db, [fornecedor_id])
    ]


def get_produtos_com_estoque_baixo_service(
    db: Session,
) -> list[ProdutoReadSucess]:
    return [
        ProdutoReadSucess.model_validate(produto)
        for produto in listar_produtos_com_estoque_baixo(db)
    ]