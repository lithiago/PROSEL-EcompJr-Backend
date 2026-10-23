from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_admin, get_current_user, get_db
from src.errors.errors import ProdutoError
from src.models.usuario import Usuario
from src.schemas.produto_schema import (
    ProdutoCreateRequest,
    ProdutoCreateSucess,
    ProdutoReadSucess,
)
from src.services.produto_service import (
    criar_produto_service,
    get_produtos_com_estoque_baixo_service,
    get_produtos_por_categoria_service,
    get_produtos_por_fornecedor_service,
    get_produtos_service,
)

produtos_router = APIRouter()


def _raise_produto_http_exception(exc: ProdutoError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    ) from exc


@produtos_router.post("/produtos", response_model=ProdutoCreateSucess, status_code=200)
def criar_produto(
    payload: ProdutoCreateRequest,
    db: Session = Depends(get_db),
    current_admin: Usuario = Depends(get_current_admin),
):
    try:
        return criar_produto_service(
            db=db,
            nome=payload.nome,
            sku_codigo=payload.sku_codigo,
            precoCusto=payload.precoCusto,
            precoVenda=payload.precoVenda,
            qtdEstoque=payload.qtdEmEstoque,
            idCategoria=payload.idCategoria,
            idFornecedor=payload.idFornecedor,
        )
    except ProdutoError as exc:
        _raise_produto_http_exception(exc)


@produtos_router.get(
    "/produtos", response_model=list[ProdutoReadSucess], status_code=200
)
def get_produtos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_produtos_service(db)
    except ProdutoError as exc:
        _raise_produto_http_exception(exc)


@produtos_router.get(
    "/produtos/{categoria_id}",
    response_model=list[ProdutoReadSucess],
    status_code=200,
)
def get_produtos_por_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_produtos_por_categoria_service(db, categoria_id)
    except ProdutoError as exc:
        _raise_produto_http_exception(exc)


@produtos_router.get(
    "/produtos/fornecedor/{fornecedor_id}",
    response_model=list[ProdutoReadSucess],
    status_code=200,
)
def get_produtos_por_fornecedor(
    fornecedor_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_produtos_por_fornecedor_service(db, fornecedor_id)
    except ProdutoError as exc:
        _raise_produto_http_exception(exc)


@produtos_router.get(
    "/produtos/estoque_minimo",
    response_model=list[ProdutoReadSucess],
    status_code=200,
)
def get_produtos_com_estoque_baixo(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return get_produtos_com_estoque_baixo_service(db)
    except ProdutoError as exc:
        _raise_produto_http_exception(exc)