from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_admin, get_current_user, get_db
from src.errors.errors import FornecedorError
from src.models.fornecedor import Fornecedor
from src.schemas.fornecedor_schema import (
    FornecedorCreateRequest,
    FornecedorCreateSucess,
    FornecedorReadSucess,
    FornecedorUpdateRequest,
)
from src.services.fornecedor_service import (
    buscar_fornecedor_por_id_service,
    buscar_fornecedores_service,
    criar_fornecedor_service,
    deletar_fornecedor_service,
    editar_fornecedor_service,
)

fornecedor_router = APIRouter()


def _raise_fornecedor_http_exception(exc: FornecedorError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    ) from exc


@fornecedor_router.post(
    "/fornecedor",
    response_model=FornecedorCreateSucess,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def criar_fornecedor(
    payload: FornecedorCreateRequest,
    db: Session = Depends(get_db),
) -> FornecedorCreateSucess:
    try:
        return criar_fornecedor_service(db=db, nome=payload.nome)
    except FornecedorError as exc:
        _raise_fornecedor_http_exception(exc)


@fornecedor_router.get(
    "/fornecedores",
    response_model=list[FornecedorReadSucess],
    dependencies=[Depends(get_current_user)],
)
def buscar_fornecedores(
    db: Session = Depends(get_db),
) -> list[Fornecedor]:
    return buscar_fornecedores_service(db)


@fornecedor_router.get(
    "/fornecedor/{fornecedor_id}",
    response_model=FornecedorReadSucess,
    dependencies=[Depends(get_current_user)],
)
def buscar_fornecedor_por_id(
    fornecedor_id: int,
    db: Session = Depends(get_db),
) -> Fornecedor:
    try:
        return buscar_fornecedor_por_id_service(db, fornecedor_id)
    except FornecedorError as exc:
        _raise_fornecedor_http_exception(exc)


@fornecedor_router.put(
    "/fornecedor/{fornecedor_id}",
    response_model=FornecedorReadSucess,
    dependencies=[Depends(get_current_admin)],
)
def editar_fornecedor(
    fornecedor_id: int,
    payload: FornecedorUpdateRequest,
    db: Session = Depends(get_db),
) -> Fornecedor:
    try:
        return editar_fornecedor_service(
            db=db,
            fornecedor_id=fornecedor_id,
            nome=payload.nome,
        )
    except FornecedorError as exc:
        _raise_fornecedor_http_exception(exc)


@fornecedor_router.delete(
    "/fornecedor/{fornecedor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def deletar_fornecedor(
    fornecedor_id: int,
    db: Session = Depends(get_db),
) -> None:
    try:
        deletar_fornecedor_service(db, fornecedor_id)
    except FornecedorError as exc:
        _raise_fornecedor_http_exception(exc)
