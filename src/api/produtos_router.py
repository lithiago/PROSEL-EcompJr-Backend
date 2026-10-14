from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_admin, get_current_user, get_db
from src.errors.errors import ProdutoError
from src.models.usuario import Usuario
from src.services.produto_service import criar_produto_service, get_produtos_service
from src.schemas.produto_schema import (
    ProdutoCreateRequest,
    ProdutoCreateSucess,
    ProdutoReadSucess,
)

produtos_router = APIRouter()


@produtos_router.post("/produtos", response_model=ProdutoCreateSucess, status_code=200)
def criar_produto(
    payload: ProdutoCreateRequest,
    request: Request,
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
        raise HTTPException(
            status_code=exc.status_code,
            detail={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )


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
        raise HTTPException(
            status_code=exc.status_code,
            detail={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )
