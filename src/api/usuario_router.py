from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_current_admin, get_db
from src.errors.errors import RegisterError, UsuarioError
from src.schemas.usuario_schema import (
    UserReadSucess,
    UserRegisterRequest,
    UserRegisterSucess,
    UserUpdateRequest,
)
from src.services.usuario_service import (
    criar_usuario_service,
    deletar_usuario_service,
    editar_usuario_service,
    get_usuario_por_id_service,
    get_usuarios_service,
)

usuario_router = APIRouter()


def _raise_register_http_exception(exc: RegisterError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    ) from exc


def _raise_usuario_http_exception(exc: UsuarioError) -> None:
    raise HTTPException(
        status_code=exc.status_code,
        detail={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    ) from exc


@usuario_router.post(
    "/usuario",
    response_model=UserRegisterSucess,
    status_code=200,
)
def criar_usuario(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> UserRegisterSucess:
    try:
        return criar_usuario_service(db, payload)
    except RegisterError as exc:
        _raise_register_http_exception(exc)


@usuario_router.get(
    "/usuarios",
    response_model=list[UserReadSucess],
    dependencies=[Depends(get_current_admin)],
)
def get_usuarios(
    db: Session = Depends(get_db),
) -> list[UserReadSucess]:
    return get_usuarios_service(db)


@usuario_router.get(
    "/usuario/{usuario_id}",
    response_model=UserReadSucess,
    dependencies=[Depends(get_current_admin)],
)
def get_usuario_por_id(
    usuario_id: int,
    db: Session = Depends(get_db),
) -> UserReadSucess:
    try:
        return get_usuario_por_id_service(db, usuario_id)
    except UsuarioError as exc:
        _raise_usuario_http_exception(exc)


@usuario_router.put(
    "/usuario/{usuario_id}",
    response_model=UserReadSucess,
    dependencies=[Depends(get_current_admin)],
)
def editar_usuario(
    usuario_id: int,
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
) -> UserReadSucess:
    try:
        return editar_usuario_service(db, usuario_id, payload)
    except UsuarioError as exc:
        _raise_usuario_http_exception(exc)


@usuario_router.delete(
    "/usuario/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
) -> Response:
    try:
        deletar_usuario_service(db, usuario_id)
    except UsuarioError as exc:
        _raise_usuario_http_exception(exc)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
