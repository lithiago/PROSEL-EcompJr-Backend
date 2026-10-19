from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_admin, get_current_user, get_db
from src.errors.errors import CategoriaError
from src.models.categoria import Categoria
from src.schemas.categoria_schema import (
    CategoriaCreateRequest,
    CategoriaReadSucess,
    CategoriaUpdateRequest,
)
from src.services.categoria_service import (
    buscar_categoria_por_id_service,
    buscar_categorias_service,
    criar_categoria_service,
    deletar_categoria_service,
    editar_categoria_service,
)

categorias_router = APIRouter()


def _raise_categoria_http_exception(exc: CategoriaError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    ) from exc


@categorias_router.post(
    "/categoria",
    response_model=CategoriaReadSucess,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def criar_categoria(
    payload: CategoriaCreateRequest,
    db: Session = Depends(get_db),
) -> Categoria:
    try:
        return criar_categoria_service(db=db, nome=payload.nome)
    except CategoriaError as exc:
        _raise_categoria_http_exception(exc)


@categorias_router.get(
    "/categorias",
    response_model=list[CategoriaReadSucess],
    dependencies=[Depends(get_current_user)],
)
def buscar_categorias(
    db: Session = Depends(get_db),
) -> list[Categoria]:
    return buscar_categorias_service(db)


@categorias_router.get(
    "/categoria/{categoria_id}",
    response_model=CategoriaReadSucess,
    dependencies=[Depends(get_current_user)],
)
def buscar_categoria_por_id(
    categoria_id: int,
    db: Session = Depends(get_db),
) -> Categoria:
    try:
        return buscar_categoria_por_id_service(db, categoria_id)
    except CategoriaError as exc:
        _raise_categoria_http_exception(exc)


@categorias_router.put(
    "/categoria/{categoria_id}",
    response_model=CategoriaReadSucess,
    dependencies=[Depends(get_current_admin)],
)
def editar_categoria(
    categoria_id: int,
    payload: CategoriaUpdateRequest,
    db: Session = Depends(get_db),
) -> Categoria:
    try:
        return editar_categoria_service(
            db=db,
            categoria_id=categoria_id,
            nome=payload.nome,
        )
    except CategoriaError as exc:
        _raise_categoria_http_exception(exc)


@categorias_router.delete(
    "/categoria/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def deletar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
) -> None:
    try:
        deletar_categoria_service(db, categoria_id)
    except CategoriaError as exc:
        _raise_categoria_http_exception(exc)
